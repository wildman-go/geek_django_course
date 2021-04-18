from django.contrib import admin
from .models import Candidate
from datetime import datetime
from django.http import HttpResponse
from interview import candidate_fieldset as cf
from django.db.models import Q

import csv
import logging

logger = logging.getLogger(__name__)

exportable_fields = (
    'username', 'city', 'phone', 'bachelor_school', 'master_school', 'degree', 'first_result', 'first_interviewer_user',
    'second_result', 'second_interviewer_user', 'hr_result', 'hr_score', 'hr_remark', 'hr_interviewer_user')


def export_model_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    field_list = exportable_fields
    response['Content-Disposition'] = 'attachment; filename=recruitment-candidates=%s.csv' % (
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    )

    # 写入表头
    writer = csv.writer(response)
    writer.writerow(
        [queryset.model._meta.get_field(f).verbose_name.title() for f in field_list]
    )
    pass

    # 将单行记录写入表中
    for query in queryset:
        csv_line_values = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(query)
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)
    logger.info('%s exported %s candidate records.' % (request.user.username, len(queryset)))
    return response


export_model_as_csv.short_description = r'导出为csv文件'
export_model_as_csv.allowed_permissions = ('export',)


# Register your models here.

class CandidateAdmin(admin.ModelAdmin):
    exclude = ('creator', 'created_date', 'modified_date')
    list_display = (
        'username', 'city', 'bachelor_school', 'first_score', 'first_result', 'first_interviewer_user',
        'second_result', 'second_interviewer_user', 'hr_score', 'hr_result', 'last_editor'
    )
    actions = [export_model_as_csv, ]

    # 判断当前用户是否有导出csv的权限
    def has_export_permission(self, request):
        opts = self.opts
        return request.usr.has_perm('%s.%s' % (opts.app_label, 'export'))

    # 添加可被搜索的字段
    search_fields = ('username', 'phone', 'email', 'bachelor_school')

    # 添加可被筛选的字段
    list_filter = ('city', 'first_result', 'second_result', 'hr_result',
                   'first_interviewer_user', 'second_interviewer_user', 'hr_interviewer_user')

    # 添加可排序的字段
    ordering = ('hr_result', 'second_result', 'first_result')

    def get_group_names(self, user):
        group_name = []
        for g in user.groups.all():
            group_name.append(g.name)
        return group_name

    # 对于非管理员，非HR，获取自己是一面或二面面试官的候选人集合
    def get_queryset(self, request):
        qs = super(CandidateAdmin, self).get_queryset(request)
        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in group_names:
            return qs
        return Candidate.objects.filter(
            Q(first_interviewer_user=request.user) | Q(second_interviewer_user=request.user))

    # 设置 面试官只读/hr可编辑 的字段
    def get_readonly_fields(self, request, obj=None):
        group_names = self.get_group_names(request.user)
        if 'interviewer' in group_names:
            logger.info("interviewer is in user's group for %s" % request.user.username)
            return ('first_interviewer_user', 'second_interviewer_user')
        return ()

    # 设置 在候选人列表页，hr可编辑/面试官只读 的字段
    def get_list_editable(self, request):
        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in group_names:
            return ('first_interviewer_user', 'second_interviewer_user')
        return ()

    def get_changelist_instance(self, request):
        self.list_editable = self.get_list_editable(request)
        return super(CandidateAdmin, self).get_changelist_instance(request)

    # 在候选人编辑页，一面面试官只能看到一面成绩，二面面试官只能看到二面成绩
    def get_fieldsets(self, request, obj=None):
        group_names = self.get_group_names(request.user)
        if 'interviewer' in group_names and obj.first_interviewer_user == request.user:
            return cf.default_fieldsets_first
        if 'interviewer' in group_names and obj.second_interviewer_user == request.user:
            return cf.default_fieldsets_second
        return cf.default_fieldsets

    def save_model(self, request, obj, form, change):
        obj.last_editor = request.user.username
        if not obj.creator:
            obj.creator = request.user.username
        obj.modified_date = datetime.now()
        obj.save()


admin.site.register(Candidate, CandidateAdmin)
