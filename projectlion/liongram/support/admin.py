from django.contrib import admin

from .models import Faq, Inquiry, Answer

class AnswerInline(admin.TabularInline):
    model = Answer

@admin.register(Faq)
class FaqModelAdmin(admin.ModelAdmin):
     # 목록페이지 출력 필드 : 제목, 카테고리, 최종 수정 일시
    list_display = ('title', 'content', 'category', 'updated_at', ) # 튜플로 작성 시 하나 작성할 때마다 끝에 콤마 붙여줘야 함
    # 검색 필드 : 제목
    search_fields = ('title', )
    # 필터 필드 : 카테고리
    list_filter = ('category', )
    
@admin.action(description='답변 완료 안내 발송')
def complete(modeladmin, request, queryset):
    for query in queryset:
        if query.is_email:
            print(f'{query.created_by} = {query.is_email}')
        if query.is_phone:
            print(f'{query.created_by} = {query.is_phone}')

@admin.action(description='일괄 접수 처리')
def complete2(modeladmin, request, queryset):
    queryset.update(status=Inquiry.STATUS_CHOICES[1][0])


@admin.register(Inquiry)
class InquiryModelAdmin(admin.ModelAdmin):
    # 목록페이지 출력 필드 : 질문 제목, 카테고리, 생성 일시, 생성자
    list_display = ('status', 'category', 'title', 'created_at', 'created_by', )
    # 검색 필드 : 제목, 이메일, 전화번호
    search_fields = ('title', 'email', 'phone', 
                     'user__username', 'user__phone', 'user__email') # lookup으로 user 모델의 속성 가져올 수 있음 ('user__속성이름')
    # 필터 필드 : 카테고리
    list_filter = ('status', 'category', )
    # 인라인 모델 : 답변('Answer')
    inlines = [AnswerInline, ]
    actions = [complete, complete2]

# @admin.register(Answer)
# class AnswerModelAdmin(admin.ModelAdmin):
#     pass