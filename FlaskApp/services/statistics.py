import calendar
from repository.posts_repository_interface import PostsRepositoryInterface
from repository.users_repository_interface import UsersRepositoryInterface


class Statistics:
    def __init__(self, users: UsersRepositoryInterface, posts: PostsRepositoryInterface):
        self.posts = posts
        self.users = users

    def get_user_statistics(self, username):
        user = self.users.get_by_name(username)
        user_posts = self.posts.get_all_by_user(user.name)
        months_dict = dict()
        for i in range(1, 13):
            months_dict[i] = 0
            for post in user_posts:
                if post.created_at.month == i:
                    months_dict[i] += 1
        sorted_tuple_months = sorted(months_dict.items(), key=lambda kv: kv[1])
        string_months = {}
        for i in range(0, 12):
            string_months[calendar.month_name[sorted_tuple_months[i][0]]] =\
            sorted_tuple_months[i][1]
        return string_months
