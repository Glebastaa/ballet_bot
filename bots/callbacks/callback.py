from aiogram import Router

from bots.callbacks import (
    callbacks_studio, callbacks_group,
    callbacks_student, callbacks_weekday,
    callbacks_user
)

router = Router()

router.include_router(callbacks_studio.router)
router.include_router(callbacks_group.router)
router.include_router(callbacks_student.router)
router.include_router(callbacks_weekday.router)
router.include_router(callbacks_user.router)
