from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('principal', 'Principal'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    email = models.EmailField(blank=True)  # Allow email to be blank
    REQUIRED_FIELDS = []

class Grade(models.Model):
    name = models.CharField(max_length=10)
    level = models.IntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} (Level {self.level})"

class Subject(models.Model):
    name = models.CharField(max_length=255)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    classroom = models.ForeignKey('Classroom', related_name='subjects', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.grade.name}"


class Classroom(models.Model):
    name = models.CharField(max_length=100)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='classrooms')
    capacity = models.IntegerField()
    class_teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='class_teacher_of')
    teachers = models.ManyToManyField('Teacher', related_name='teaching_classes', blank=True)
    total_students = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='student')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    adhar_num = models.CharField(max_length=12, unique=True)
    admission_date = models.DateField()
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='students')
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    performance = models.TextField(blank=True)
    attendance_records = models.TextField(blank=True)
    disciplinary_actions = models.TextField(blank=True)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_fee = models.DecimalField(max_digits=10, decimal_places=2)
    attendance_percentage = models.FloatField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    roll_number = models.CharField(max_length=20, unique=True, blank=True, null=True)

    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    initial_setup_complete = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.roll_number:
            last_student = Student.objects.filter(grade=self.grade).order_by('-roll_number').first()
            if last_student and last_student.roll_number:
                next_roll_number = int(last_student.roll_number[-2:]) + 1
            else:
                next_roll_number = 1
            self.roll_number = f"{self.grade.level:02d}{str(next_roll_number).zfill(2)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.roll_number})"

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    class_teacher_of_grade =models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL)
    main_subject = models.CharField(max_length=100)  # New field
    extra_subjects = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()

class Principal(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()

class Notification(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Attendance(models.Model):
    ATTENDANCE_STATUS = [
        (0, 'Absent'),
        (1, 'Present'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    class_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='class_attendances')
    date = models.DateField(default=timezone.now)
    status = models.IntegerField(choices=ATTENDANCE_STATUS)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.class_teacher:
            self.class_teacher = Teacher.objects.filter(class_teacher_of_grade=self.student.grade).first()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.date} - {self.get_status_display()}"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=200)
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Exam(models.Model):
    name = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    date = models.DateField()
    duration = models.DurationField()

    def __str__(self):
        return self.name

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    marks_obtained = models.FloatField()
    grade = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.student} - {self.exam} - {self.marks_obtained}"

class Homework(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    assigned_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='homeworks')
    assigned_by = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='homeworks')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='homeworks')

    def __str__(self):
        return self.title

class Parent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='parent_profile')
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.get_full_name()






class TeacherSubjectAssignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)









from django.db import models
from django.conf import settings

class Complaint(models.Model):
    TOPIC_CHOICES = [
        ('academic', 'Academic'),
        ('behavior', 'Behavior'),
        ('facility', 'Facility'),
        ('other', 'Other'),
    ]

    topic = models.CharField(max_length=100, choices=TOPIC_CHOICES)
    description = models.TextField()
    complainant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_filed = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    resolution_date = models.DateTimeField(null=True, blank=True)
    complainant_role = models.CharField(max_length=10)  # new field to store the role

    def __str__(self):
        return f"{self.topic} - {self.complainant.username} ({self.complainant_role})"
