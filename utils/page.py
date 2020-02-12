# -*- coding:utf-8 -*-
# Author:cqk
# Data:2019/10/21 14:31
from django.utils.safestring import mark_safe


class InitPage:
    """
    分页组件
    """

    def __init__(self, current_page, data_length, show_data_number=10, show_page_number=7,get_data=None):
        """

        :param current_page:当前页码
        :param data_length: 总数据数量
        :param show_data_number: 每页展示数据量
        :param show_page_number: 显示页码个数
        :param get_data: 可变的QueryDict对象  里面有 page = x
        total_page_count: 页码总数
        start_page_number:起始页码
        end_page_number:结束页码

        """

        self.get_data=get_data
        try:
            current_page=int(current_page)  # 保证页码是整数
        except Exception:
            current_page=1
        a, b=divmod(data_length, show_data_number)
        # 如果余数不为0，页码总数为商+1
        if b:
            total_page_count=a + 1
        else:
            total_page_count=a
        # 将页码控制在页码总数范围之内
        if current_page <= 0:
            current_page=1
        elif current_page >= total_page_count:
            current_page=total_page_count

        if total_page_count < show_page_number:  # 页码总数小于展示页码总数的情况
            start_page_number=1
            end_page_number=total_page_count+1
        else:
            half_number=show_page_number // 2
            start_page_number=current_page - half_number
            end_page_number=current_page + half_number + 1
            if start_page_number <= 0:
                start_page_number=1
                end_page_number=show_page_number + 1
            elif end_page_number >= total_page_count:
                end_page_number=total_page_count+1
                start_page_number=total_page_count - show_page_number + 1
        if current_page:
            self.start_page_number=start_page_number
            self.end_page_number=end_page_number
            self.total_page_count=total_page_count
            self.current_page=current_page
            self.data_length=data_length
            self.show_data_number=show_data_number
            self.show_page_number=show_page_number
        else:
            self.start_page_number=1
            self.end_page_number=1
            self.total_page_count=1
            self.current_page=1
            self.data_length=0
            self.show_data_number=show_data_number
            self.show_page_number=show_page_number

    @property
    def start_data_number(self):

        return (self.current_page - 1) * self.show_data_number

    @property
    def end_data_number(self):

        return self.current_page * self.show_data_number
    def page_html_func(self):
        if self.data_length:
            page_html='''
                       <nav aria-label="Page navigation">
                         <ul class="pagination">
                       '''
            self.get_data["page"]=1
            first_page=f'''
                           <li>
                             <a href="?{self.get_data.urlencode()}" aria-label="Previous">
                               <span aria-hidden="true">首页</span>
                             </a>
                           </li>
                      '''
            page_html+=first_page
            self.get_data["page"]=self.current_page - 1
            previous_page=f'''
                       <li>
                             <a href="?{self.get_data.urlencode()}" aria-label="Previous">
                               <span aria-hidden="true">&laquo;</span>
                             </a>
                           </li>'''
            page_html+=previous_page

            for i in range(self.start_page_number, self.end_page_number):
                self.get_data["page"]=i
                if i == self.current_page:

                    page_html+=f'<li class="active"><a href="?{self.get_data.urlencode()}">{i}</a></li>'
                else:
                    page_html+=f'<li><a href="?{self.get_data.urlencode()}">{i}</a></li>'
            self.get_data["page"]=self.current_page + 1
            next_page=f"""
                           <li>
                                 <a href="?{self.get_data.urlencode()}" aria-label="Next">
                                   <span aria-hidden="true">&raquo;</span>
                                 </a>
                               </li>
               """
            page_html+=next_page
            self.get_data["page"]=self.total_page_count
            last_page=f"""
                               <li>
                                 <a href="?{ self.get_data.urlencode()}" aria-label="Previous">
                                   <span aria-hidden="true">尾页</span>
                                 </a>
                               </li>"""
            page_html+=last_page

            page_html+="""
    
                             </ul>
                           </nav>
                       """
            return mark_safe(page_html)
        return "暂无此信息!"
