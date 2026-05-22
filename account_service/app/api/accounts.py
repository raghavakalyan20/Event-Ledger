from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Account, Transaction
from app.schemas.account import TransactionRequest

router = APIRouter()


@router.post("/accounts/{account_id}/transactions")
def apply_transaction(
    account_id: str,
    request: TransactionRequest,
    db: Session = Depends(get_db)
):
    existing_txn = db.query(Transaction).filter(
        Transaction.event_id == request.eventId
    ).first()

    if existing_txn:
        return {
            "message": "Duplicate transaction ignored",
            "eventId": request.eventId
        }

    account = db.query(Account).filter(
        Account.account_id == account_id
    ).first()

    if not account:
        account = Account(
            account_id=account_id,
            balance=0.0
        )
        db.add(account)
        db.commit()
        db.refresh(account)

    if request.type == "CREDIT":
        account.balance += request.amount
    else:
        account.balance -= request.amount

    txn = Transaction(
        event_id=request.eventId,
        account_id=request.accountId,
        type=request.type,
        amount=request.amount
    )

    db.add(txn)
    db.commit()
    db.refresh(account)

    return {
        "accountId": account.account_id,
        "balance": account.balance,
        "message": "Transaction applied"
    }


@router.get("/accounts/{account_id}/balance")
def get_balance(
    account_id: str,
    db: Session = Depends(get_db)
):
    account = db.query(Account).filter(
        Account.account_id == account_id
    ).first()

    if not account:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    return {
        "accountId": account.account_id,
        "balance": account.balance
    }


@router.get("/accounts/{account_id}")
def get_account_details(
    account_id: str,
    db: Session = Depends(get_db)
):
    account = db.query(Account).filter(
        Account.account_id == account_id
    ).first()

    if not account:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    transactions = db.query(Transaction).filter(
        Transaction.account_id == account_id
    ).all()

    return {
        "accountId": account.account_id,
        "balance": account.balance,
        "transactions": [
            {
                "eventId": txn.event_id,
                "type": txn.type,
                "amount": txn.amount
            }
            for txn in transactions
        ]
    }


@router.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "account-service"
    }