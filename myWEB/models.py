from django.db import models


# Create your models here.


class CalculatorTable(models.Model):  # 计算器计算结果表
    value_A = models.CharField(max_length=10)
    value_B = models.CharField(max_length=10)
    value_C = models.CharField(max_length=10)


class CollegeTable(models.Model):  # 院系表
    yxh = models.CharField(max_length=10, primary_key=True)  # 院系号
    mc = models.CharField(max_length=20, blank=False)  # 名称


class StudentTable(models.Model):  # 学生表
    xh = models.CharField(max_length=20, primary_key=True)  # 学号
    xm = models.CharField(max_length=10, blank=False)  # 姓名
    yxh = models.ForeignKey(CollegeTable, on_delete=models.CASCADE)  # 院系号
    yydj = models.CharField(max_length=10)  # 英语等级


class TeacherTable(models.Model):  # 教师表
    gh = models.CharField(max_length=20, primary_key=True)  # 工号
    xm = models.CharField(max_length=10, blank=False)  # 姓名
    yxh = models.ForeignKey(CollegeTable, on_delete=models.CASCADE)  # 院系号
    xl = models.CharField(max_length=10)  # 学历


class ClassTable(models.Model):  # 开课表
    xq = models.CharField(max_length=20, blank=False)  # 学期
    kh = models.CharField(max_length=20, blank=False)  # 课号
    km = models.CharField(max_length=20, blank=False)  # 课名
    gh = models.ForeignKey(TeacherTable, on_delete=models.CASCADE)  # 工号
    sksj = models.CharField(max_length=20, blank=False)  # 上课时间


class ScoreTable(models.Model):  # 选课表
    xh = models.ForeignKey(StudentTable, on_delete=models.CASCADE)  # 学号
    xq = models.CharField(max_length=20, blank=False)  # 学期
    kh = models.ForeignKey(ClassTable, on_delete=models.CASCADE)  # 课号
    gh = models.ForeignKey(TeacherTable, on_delete=models.CASCADE)  # 工号
    pscj = models.FloatField()  # 平时成绩
    kscj = models.FloatField()  # 考试成绩
    zpcj = models.FloatField()  # 总评成绩
