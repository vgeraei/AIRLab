# # Create your tasks here
# from __future__ import absolute_import, unicode_literals
# from celery import shared_task, task
#
#
# @shared_task
# def add(x, y):
#     return x + y
#
#
# @shared_task
# def mul(x, y):
#     return x * y
#
#
# @shared_task
# def xsum(numbers):
#     return sum(numbers)
#
# @task()
# def print_it(str):
#     while True:
#         print(str)
#
# #
# # @app.task(bind=True)
# # def dump_context(self, x, y):
# #     print('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(
# #             self.request))
#
# #
# # if __name__ == "__main__":
# #     print("celery is running")