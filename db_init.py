from src.app.infrastructure.db.database import engine
import src.app.domain as domain

domain.Base.metadata.create_all(bind=engine)