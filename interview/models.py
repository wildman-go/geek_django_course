from django.db import models
from django.contrib.auth.models import User

# 第一轮面试结果
FIRST_INTERVIEW_RESULT_TYPE = [('建议复试', '建议复试'), ('待定', '待定'), ('放弃', '放弃'), ]
# 复试面试建议
INTERVIEW_RESULT_TYPE = [('建议录用', '建议录用'), ('待定', '待定'), ('放弃', '放弃'), ]
# HR终面结论
HR_SCORE_TYPE = [('S', 'S'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ]
# 候选人学历
DEGREE_TYPE = [('本科', '本科'), ('硕士', '硕士'), ('博士', '博士')]


# Create your models here.


class Candidate(models.Model):
    # 基础信息
    userid = models.IntegerField(unique=True, blank=True, null=True, verbose_name=r'应聘者ID')
    username = models.CharField(max_length=135, verbose_name=r'姓名')
    city = models.CharField(max_length=135, verbose_name=r'城市')
    phone = models.CharField(max_length=135, verbose_name=r'手机号码')
    email = models.CharField(max_length=135, blank=True, verbose_name=r'邮箱地址')
    apply_position = models.CharField(max_length=135, blank=True, verbose_name=r'应聘职位')
    born_address = models.CharField(max_length=135, blank=True, verbose_name=r'生源地')
    gender = models.CharField(max_length=135, blank=True, verbose_name=r'性别')
    candidate_remark = models.CharField(max_length=135, blank=True, verbose_name=r'候选人备注信息')

    # 学校与学历信息
    bachelor_school = models.CharField(max_length=135, blank=True, verbose_name=r'本科学校')
    master_school = models.CharField(max_length=135, blank=True, verbose_name=r'研究生学校')
    doctor_school = models.CharField(max_length=135, blank=True, verbose_name=r'博士生学校')
    major = models.CharField(max_length=135, blank=True, verbose_name=r'专业')
    degree = models.CharField(max_length=135, choices=DEGREE_TYPE, blank=True, verbose_name=r'学历')

    # 综合能力测评成绩，笔试测评成绩
    test_score_of_general_ability = models.DecimalField(decimal_places=1, null=True, max_digits=3, blank=True,
                                                        verbose_name=r'综合能力测评成绩')
    paper_score = models.DecimalField(decimal_places=1, null=True, max_digits=3, blank=True, verbose_name=r'笔试成绩')

    # 第一轮面试记录
    first_score = models.DecimalField(decimal_places=1, null=True, max_digits=2, blank=True, verbose_name=r'初试分',
                                      help_text=r'1-5分，极优秀:>=4.5，优秀:4-4.4，良好:3.5-3.9,一般:3-3.4,较差:<3')
    first_learning_ability = models.DecimalField(decimal_places=1, null=True, max_digits=2, blank=True,
                                                 verbose_name=r'学习能力得分')
    first_professional_competency = models.DecimalField(decimal_places=1, null=True, max_digits=2, blank=True,
                                                        verbose_name=r'专业能力得分')
    first_advantage = models.TextField(max_length=1024, blank=True, verbose_name=r'优势')
    first_disadvantage = models.TextField(max_length=1024, blank=True, verbose_name=r'顾虑和不足')
    first_result = models.CharField(max_length=256,
                                    choices=FIRST_INTERVIEW_RESULT_TYPE, blank=True, verbose_name=r'初试结果')
    first_recommend_position = models.CharField(max_length=256, blank=True, verbose_name=r'推荐部门')
    first_interviewer_user = models.ForeignKey(User, related_name=r'first_interviewer_user', blank=True, null=True,
                                               on_delete=models.CASCADE, verbose_name=r'一面面试官')
    first_remark = models.CharField(max_length=135, blank=True, verbose_name=r'初试备注')

    # 第二轮面试记录
    second_score = models.DecimalField(decimal_places=1, null=True, max_digits=2, blank=True, verbose_name=r'专业复试得分',
                                       help_text=r'1-5分，极优秀:>=4.5，优秀:4-4.4，良好:3.5-3.9,一般:3-3.4,较差:<3')
    second_learning_ability = models.DecimalField(decimal_places=1, null=True, max_digits=2, blank=True,
                                                  verbose_name=r'学习能力得分')
    second_professional_competency = models.DecimalField(decimal_places=1, null=True, max_digits=2, blank=True,
                                                         verbose_name=r'专业能力得分')
    second_pursue_of_excellence = models.DecimalField(decimal_places=1, null=True, max_digits=2, blank=True,
                                                      verbose_name=r'追求卓越得分')
    second_communication_ability = models.DecimalField(decimal_places=1, null=True, max_digits=2, blank=True,
                                                       verbose_name=r'沟通能力得分')
    second_pressure_score = models.DecimalField(decimal_places=1, null=True, max_digits=2, blank=True,
                                                verbose_name=r'抗压能力得分')
    second_advantage = models.TextField(max_length=1024, blank=True, verbose_name=r'优势')
    second_disadvantage = models.TextField(max_length=1024, blank=True, verbose_name=r'顾虑和不足')
    second_result = models.CharField(max_length=256,
                                     choices=INTERVIEW_RESULT_TYPE, blank=True, verbose_name=r'专业复试结果')
    second_recommend_position = models.CharField(max_length=256, blank=True, verbose_name=r'建议方向或推荐部门')
    second_interviewer_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                                                related_name=r'second_interviewer_user', verbose_name=r'二面面试官')
    second_remark = models.CharField(max_length=135, blank=True, verbose_name=r'专业复试备注')

    # hr终面
    hr_score = models.CharField(max_length=10, choices=HR_SCORE_TYPE, blank=True, verbose_name=r'HR复试综合等级',
                                help_text=r'1-5分，极优秀:>=4.5，优秀:4-4.4，良好:3.5-3.9,一般:3-3.4,较差:<3')
    hr_responsibility = models.CharField(max_length=10, choices=HR_SCORE_TYPE, blank=True, verbose_name=r'HR责任心')
    hr_communication_ability = models.CharField(max_length=10, choices=HR_SCORE_TYPE, blank=True,
                                                verbose_name=r'HR坦诚沟通')
    hr_logic_ability = models.CharField(max_length=10, choices=HR_SCORE_TYPE, blank=True, verbose_name=r'HR逻辑思维')
    hr_potential = models.CharField(max_length=10, choices=HR_SCORE_TYPE, blank=True, verbose_name=r'HR发展潜力')
    hr_stability = models.CharField(max_length=10, choices=HR_SCORE_TYPE, blank=True, verbose_name=r'HR稳定性')
    hr_advantage = models.TextField(max_length=1024, blank=True, verbose_name=r'优势')
    hr_disadvantage = models.TextField(max_length=1024, blank=True, verbose_name=r'顾虑和不足')
    hr_result = models.CharField(max_length=256,
                                 choices=INTERVIEW_RESULT_TYPE, blank=True, verbose_name=r'HR复试结果')
    hr_interviewer_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                                            related_name=r'hr_interviewer_user', verbose_name=r'HR面试官')
    hr_remark = models.CharField(max_length=135, blank=True, verbose_name=r'HR复试备注')

    creator = models.CharField(max_length=256, blank=True, verbose_name=r'候选人数据的创建人')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=r'创建时间')
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name=r'更新时间')
    last_editor = models.CharField(max_length=256, blank=True, verbose_name=r'最后编辑者')

    class Meta:
        db_table = r'candidate'
        verbose_name = r'应聘者'
        verbose_name_plural = r'应聘者'

        permissions = [
            ("export", "Can export candidate list"),
        ]

    def __str__(self):
        return self.username
