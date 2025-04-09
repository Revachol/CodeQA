from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike

from django.utils.crypto import get_random_string
from django.utils import timezone
from random import choice, randint, sample


class Command(BaseCommand):
    help = 'Fill database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Scaling ratio')

    def handle(self, *args, **options):
        ratio = options['ratio']

        num_users = ratio
        num_tags = ratio
        num_questions = ratio * 10
        num_answers = ratio * 100
        num_likes = ratio * 200

        self.stdout.write(f"Filling database with ratio={ratio}")

        # USERS & PROFILES
        users = [
            User(username=f'user_{i}', email=f'user_{i}@mail.com')
            for i in range(num_users)
        ]
        User.objects.bulk_create(users)
        created_users = list(User.objects.filter(username__startswith='user_'))
        profiles = [Profile(user=user) for user in created_users]
        Profile.objects.bulk_create(profiles)
        profiles = list(Profile.objects.select_related('user').filter(user__username__startswith='user_'))

        # TAGS
        tags = [Tag(name=f'tag_{i}') for i in range(num_tags)]
        Tag.objects.bulk_create(tags)
        tags = list(Tag.objects.all())

        # QUESTIONS
        questions = [
            Question(
                title=f'Question {i}',
                text='Sample question text',
                author=choice(profiles),
            ) for i in range(num_questions)
        ]
        Question.objects.bulk_create(questions)
        questions = list(Question.objects.all())

        for q in questions:
            q.tags.add(*sample(tags, k=randint(1, 3)))

        # ANSWERS
        answers = [
            Answer(
                question=choice(questions),
                text='Sample answer text',
                author=choice(profiles),
                is_correct=False
            ) for _ in range(num_answers)
        ]
        Answer.objects.bulk_create(answers)
        answers = list(Answer.objects.all())

        # QUESTION LIKES
        qlikes = []
        for _ in range(num_likes):
            profile = choice(profiles)
            question = choice(questions)
            qlikes.append(QuestionLike(user=profile, question=question, value=1))
        QuestionLike.objects.bulk_create(qlikes, ignore_conflicts=True)

        # ANSWER LIKES
        alikes = []
        for _ in range(num_likes):
            profile = choice(profiles)
            answer = choice(answers)
            alikes.append(AnswerLike(user=profile, answer=answer, value=1))
        AnswerLike.objects.bulk_create(alikes, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS('Successfully filled database!'))
