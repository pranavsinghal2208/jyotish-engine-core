from fastapi import APIRouter, Depends
from ..core.identity import get_identity
from ..core.context import CosmicContext
from ..core.registry import registry
from ..database.models import User

router = APIRouter(prefix="/api/v2")

@router.get("/intelligence")
async def get_all_intelligence(user: User = Depends(get_identity)):
    """Unified endpoint to fetch all registered capabilities."""
    ctx = CosmicContext(user)
    return registry.get_all(ctx)
from fastapi import Response
from ..services.cosmic_id import generate_cosmic_id_svg

@router.get("/share/cosmic-id.svg")
async def get_cosmic_id(user: User = Depends(get_identity)):
    """Returns the highly shareable Cosmic ID SVG."""
    ctx = CosmicContext(user)
    svg_content = generate_cosmic_id_svg(ctx)
    return Response(content=svg_content, media_type="image/svg+xml")
