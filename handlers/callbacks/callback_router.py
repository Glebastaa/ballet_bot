from aiogram import Router

from handlers.callbacks import (
    studio, student, schedule, group, user, weekday
)


router = Router()

router.include_router(studio.router)
router.include_router(student.router)
#router.include_router(schedule.router)
router.include_router(group.router)
#router.include_router(user.router)
router.include_router(weekday.router)
