from aiogram import Router

from handlers.state_handlers import (
    studio, student, group, user
)


router = Router()

router.include_router(studio.router)
router.include_router(student.router)
router.include_router(group.router)
router.include_router(user.router)
