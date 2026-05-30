from fastapi import FastAPI, HTTPException
from database import engine, SessionLocal
from models import Base, Expense
from schemas import ExpenseCreate

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Expense Tracker API Running"}


@app.post("/expenses")
def add_expense(expense: ExpenseCreate):

    db = SessionLocal()

    new_expense = Expense(
        category=expense.category,
        amount=expense.amount
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    db.close()

    return {
        "message": "Expense added successfully"
    }


@app.get("/expenses")
def get_expenses():

    db = SessionLocal()

    expenses = db.query(Expense).all()

    result = []

    for expense in expenses:
        result.append({
            "id": expense.id,
            "category": expense.category,
            "amount": expense.amount
        })

    db.close()

    return result


@app.get("/expenses/highest")
def highest_expense():

    db = SessionLocal()

    expenses = db.query(Expense).all()

    if not expenses:
        db.close()
        return {"message": "No expenses found"}

    highest = max(expenses, key=lambda x: x.amount)

    result = {
        "id": highest.id,
        "category": highest.category,
        "amount": highest.amount
    }

    db.close()

    return result

@app.put("/expenses/{expense_id}")
def update_expense(
    expense_id: int,
    updated_data: ExpenseCreate
):

    db = SessionLocal()

    expense = db.query(Expense).filter(
        Expense.id == expense_id
    ).first()

    if not expense:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    expense.category = updated_data.category
    expense.amount = updated_data.amount

    db.commit()

    db.close()

    return {
        "message": "Expense updated successfully"
    }

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):

    db = SessionLocal()

    expense = db.query(Expense).filter(
        Expense.id == expense_id
    ).first()

    if not expense:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    db.delete(expense)
    db.commit()

    db.close()

    return {
        "message": "Expense deleted successfully"
    }

@app.get("/expenses/total")
def total_expense():

    db = SessionLocal()

    expenses = db.query(Expense).all()

    total = sum(
        expense.amount
        for expense in expenses
    )

    db.close()

    return {
        "total": total
    }

@app.get("/expenses/category/{category}")
def get_by_category(category: str):

    db = SessionLocal()

    expenses = db.query(Expense).filter(
        Expense.category == category
    ).all()

    result = []

    for expense in expenses:
        result.append({
            "id": expense.id,
            "category": expense.category,
            "amount": expense.amount
        })

    db.close()

    return result