from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from pydantic import BaseModel
from typing import List, Optional
from models.database import get_db, User, Artwork, Like, Comment
from utils.auth import verify_token
from utils.ai_generator import ai_generator

router = APIRouter(prefix="/artworks", tags=["artworks"])

class ArtworkCreate(BaseModel):
    title: str
    prompt: str
    negative_prompt: Optional[str] = None
    guidance_scale: float = 7.5
    width: int = 512
    height: int = 512
    is_public: bool = True

class ArtworkResponse(BaseModel):
    id: int
    title: str
    prompt: str
    image_url: str
    creator_username: str
    likes_count: int
    comments_count: int
    is_featured: bool
    created_at: str

class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    content: str
    username: str
    created_at: str

def get_current_user(username: str = Depends(verify_token), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/generate", response_model=ArtworkResponse)
async def generate_artwork(
    artwork: ArtworkCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Generate AI artwork
        image_path, filename = await ai_generator.generate_image(
            prompt=artwork.prompt,
            negative_prompt=artwork.negative_prompt,
            guidance_scale=artwork.guidance_scale,
            width=artwork.width,
            height=artwork.height
        )
        
        # Save to database
        db_artwork = Artwork(
            title=artwork.title,
            prompt=artwork.prompt,
            negative_prompt=artwork.negative_prompt,
            image_path=image_path,
            image_url=f"/static/images/{filename}",
            guidance_scale=artwork.guidance_scale,
            width=artwork.width,
            height=artwork.height,
            is_public=artwork.is_public,
            creator_id=current_user.id
        )
        
        db.add(db_artwork)
        db.commit()
        db.refresh(db_artwork)
        
        return ArtworkResponse(
            id=db_artwork.id,
            title=db_artwork.title,
            prompt=db_artwork.prompt,
            image_url=db_artwork.image_url,
            creator_username=current_user.username,
            likes_count=0,
            comments_count=0,
            is_featured=db_artwork.is_featured,
            created_at=db_artwork.created_at.isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/gallery", response_model=List[ArtworkResponse])
async def get_gallery(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100),
    featured_only: bool = False,
    db: Session = Depends(get_db)
):
    query = db.query(Artwork).filter(Artwork.is_public == True)
    
    if featured_only:
        query = query.filter(Artwork.is_featured == True)
    
    artworks = query.order_by(desc(Artwork.created_at)).offset(skip).limit(limit).all()
    
    result = []
    for artwork in artworks:
        likes_count = db.query(Like).filter(Like.artwork_id == artwork.id).count()
        comments_count = db.query(Comment).filter(Comment.artwork_id == artwork.id).count()
        
        result.append(ArtworkResponse(
            id=artwork.id,
            title=artwork.title,
            prompt=artwork.prompt,
            image_url=artwork.image_url,
            creator_username=artwork.creator.username,
            likes_count=likes_count,
            comments_count=comments_count,
            is_featured=artwork.is_featured,
            created_at=artwork.created_at.isoformat()
        ))
    
    return result

@router.get("/my-gallery", response_model=List[ArtworkResponse])
async def get_my_gallery(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    artworks = db.query(Artwork).filter(Artwork.creator_id == current_user.id).order_by(desc(Artwork.created_at)).all()
    
    result = []
    for artwork in artworks:
        likes_count = db.query(Like).filter(Like.artwork_id == artwork.id).count()
        comments_count = db.query(Comment).filter(Comment.artwork_id == artwork.id).count()
        
        result.append(ArtworkResponse(
            id=artwork.id,
            title=artwork.title,
            prompt=artwork.prompt,
            image_url=artwork.image_url,
            creator_username=current_user.username,
            likes_count=likes_count,
            comments_count=comments_count,
            is_featured=artwork.is_featured,
            created_at=artwork.created_at.isoformat()
        ))
    
    return result

@router.post("/{artwork_id}/like")
async def toggle_like(
    artwork_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    artwork = db.query(Artwork).filter(Artwork.id == artwork_id).first()
    if not artwork:
        raise HTTPException(status_code=404, detail="Artwork not found")
    
    existing_like = db.query(Like).filter(
        Like.user_id == current_user.id,
        Like.artwork_id == artwork_id
    ).first()
    
    if existing_like:
        db.delete(existing_like)
        liked = False
    else:
        new_like = Like(user_id=current_user.id, artwork_id=artwork_id)
        db.add(new_like)
        liked = True
    
    db.commit()
    likes_count = db.query(Like).filter(Like.artwork_id == artwork_id).count()
    
    return {"liked": liked, "likes_count": likes_count}

@router.post("/{artwork_id}/comments", response_model=CommentResponse)
async def add_comment(
    artwork_id: int,
    comment: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    artwork = db.query(Artwork).filter(Artwork.id == artwork_id).first()
    if not artwork:
        raise HTTPException(status_code=404, detail="Artwork not found")
    
    db_comment = Comment(
        content=comment.content,
        user_id=current_user.id,
        artwork_id=artwork_id
    )
    
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    
    return CommentResponse(
        id=db_comment.id,
        content=db_comment.content,
        username=current_user.username,
        created_at=db_comment.created_at.isoformat()
    )

@router.get("/{artwork_id}/comments", response_model=List[CommentResponse])
async def get_comments(artwork_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.artwork_id == artwork_id).order_by(desc(Comment.created_at)).all()
    
    return [
        CommentResponse(
            id=comment.id,
            content=comment.content,
            username=comment.user.username,
            created_at=comment.created_at.isoformat()
        )
        for comment in comments
    ]