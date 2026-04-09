from models.record import doc_to_record_res

async def get_dashboard_summary(db):
    pipeline_totals = [
        {
            "$group": {
                "_id": "$type",
                "total": {"$sum": "$amount"}
            }
        }
    ]
    cursor_totals = db["financial_records"].aggregate(pipeline_totals)
    totals_docs = await cursor_totals.to_list(length=None)
    
    total_income = 0
    total_expense = 0
    for doc in totals_docs:
        if doc["_id"] == "income":
            total_income = doc["total"]
        elif doc["_id"] == "expense":
            total_expense = doc["total"]
            
    net_balance = total_income - total_expense

    pipeline_category = [
        {
            "$group": {
                "_id": {"type": "$type", "category": "$category"},
                "total": {"$sum": "$amount"}
            }
        }
    ]
    cursor_category = db["financial_records"].aggregate(pipeline_category)
    category_docs = await cursor_category.to_list(length=None)
    
    category_totals = {
        "income": {},
        "expense": {}
    }
    for doc in category_docs:
        t = doc["_id"]["type"]
        cat = doc["_id"]["category"]
        category_totals[t][cat] = doc["total"]

    pipeline_monthly = [
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$date"},
                    "month": {"$month": "$date"},
                    "type": "$type"
                },
                "total": {"$sum": "$amount"}
            }
        },
        {"$sort": {"_id.year": 1, "_id.month": 1}}
    ]
    cursor_monthly = db["financial_records"].aggregate(pipeline_monthly)
    monthly_docs = await cursor_monthly.to_list(length=None)
    
    monthly_summary = []
    for doc in monthly_docs:
        monthly_summary.append({
            "year": doc["_id"]["year"],
            "month": doc["_id"]["month"],
            "type": doc["_id"]["type"],
            "total": doc["total"]
        })

    cursor_recent = db["financial_records"].find({}).sort("date", -1).limit(5)
    recent_docs = await cursor_recent.to_list(length=5)
    recent_transactions = [doc_to_record_res(doc) for doc in recent_docs]

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": net_balance,
        "category_wise_totals": category_totals,
        "monthly_summary": monthly_summary,
        "recent_transactions": recent_transactions
    }
