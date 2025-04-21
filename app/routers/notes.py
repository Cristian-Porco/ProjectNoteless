from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.note import Note, NoteVersion
from app.models.category import Category
from app.schemas.note import NoteCreate, NoteOut
from app.schemas.category import CategoryAssign
from datetime import datetime
from typing import List

router = APIRouter()

@router.post("/", response_model=NoteOut)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    db_note = Note(title=note.title, is_public=note.is_public, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    version = NoteVersion(content=note.content, note_id=db_note.id)
    db.add(version)
    if note.category_ids:
        categories = db.query(Category).filter(Category.id.in_(note.category_ids)).all()
        db_note.categories.extend(categories)
    db.commit()
    return db_note

@router.get("/", response_model=List[NoteOut])
def list_notes(db: Session = Depends(get_db)):
    notes = db.query(Note).all()
    return notes

@router.get("/{note_id}", response_model=NoteOut)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.post("/{note_id}/categories")
def assign_categories_to_note(note_id: int, category_data: CategoryAssign, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    categories = db.query(Category).filter(Category.id.in_(category_data.category_ids)).all()
    note.categories = categories
    db.commit()
    return {"message": "Categories assigned successfully"}
