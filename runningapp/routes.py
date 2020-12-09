from runningapp.resources.training import Training, TrainingList
from runningapp.resources.user import (
    User,
    UserRegister,
    UserList,
    UserLogin,
    UserLogout,
    ChangePassword,
    UserProfile,
)
from runningapp.resources.calculator import BmiCalculator, CaloricNeedsCalculator
from runningapp.resources.admin import AdminManageUser, AdminManageUserList
from runningapp.resources.stats import RegisteredUsersResource, KilometersRunResource, CaloriesBurntResource


def initialize_routes(api):
    """Initialize all the routes"""

    api.add_resource(UserList, "/users")
    api.add_resource(User, "/users/<int:user_id>")
    api.add_resource(UserProfile, "/userprofiles/<int:userprofile_id>")
    api.add_resource(UserRegister, "/register")
    api.add_resource(UserLogin, "/login")
    api.add_resource(UserLogout, "/logout")
    api.add_resource(ChangePassword, "/change-password")
    api.add_resource(Training, "/trainings/<int:training_id>")
    api.add_resource(TrainingList, "/trainings")
    api.add_resource(BmiCalculator, "/bmi")
    api.add_resource(CaloricNeedsCalculator, "/daily-calories")
    api.add_resource(AdminManageUserList, "/admin/users")
    api.add_resource(AdminManageUser, "/admin/users/<int:user_id>")
    api.add_resource(RegisteredUsersResource, "/total-users-number")
    api.add_resource(KilometersRunResource, "/total-kilometers-number")
    api.add_resource(CaloriesBurntResource, "/total-calories-number")
