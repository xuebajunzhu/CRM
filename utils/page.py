# -*- coding: utf-8 -*-
"""
Pagination utility for Django applications.
Provides a reusable pagination component with customizable display options.
"""
from django.utils.safestring import mark_safe


class InitPage:
    """
    Pagination component for displaying large datasets across multiple pages.
    
    Attributes:
        current_page: Current page number
        data_length: Total number of records
        show_data_number: Number of items per page
        show_page_number: Number of page links to display
        get_data: QueryDict containing GET parameters
    """

    def __init__(self, current_page, data_length, show_data_number=10, 
                 show_page_number=7, get_data=None):
        """
        Initialize pagination component.
        
        Args:
            current_page: Current page number (1-indexed)
            data_length: Total number of records in dataset
            show_data_number: Number of items to display per page (default: 10)
            show_page_number: Number of page links to show (default: 7)
            get_data: Copy of request.GET for preserving query parameters
        """
        self.get_data = get_data
        
        # Validate and normalize current page
        try:
            current_page = int(current_page)
        except (ValueError, TypeError):
            current_page = 1
        
        # Calculate total pages
        quotient, remainder = divmod(data_length, show_data_number)
        total_page_count = quotient + 1 if remainder else quotient
        
        # Ensure current page is within valid range
        current_page = max(1, min(current_page, total_page_count)) if total_page_count else 1
        
        # Calculate page range to display
        if total_page_count < show_page_number:
            start_page_number = 1
            end_page_number = total_page_count + 1
        else:
            half_range = show_page_number // 2
            start_page_number = current_page - half_range
            end_page_number = current_page + half_range + 1
            
            # Adjust range if it exceeds boundaries
            if start_page_number <= 0:
                start_page_number = 1
                end_page_number = show_page_number + 1
            elif end_page_number > total_page_count:
                end_page_number = total_page_count + 1
                start_page_number = total_page_count - show_page_number + 1
        
        # Store pagination state
        self.current_page = current_page
        self.total_page_count = total_page_count
        self.start_page_number = start_page_number
        self.end_page_number = end_page_number
        self.data_length = data_length
        self.show_data_number = show_data_number
        self.show_page_number = show_page_number

    @property
    def start_data_number(self):
        """Calculate starting index for current page."""
        return (self.current_page - 1) * self.show_data_number

    @property
    def end_data_number(self):
        """Calculate ending index for current page."""
        return self.current_page * self.show_data_number

    def page_html_func(self):
        """
        Generate HTML pagination control.
        
        Returns:
            Safe HTML string containing pagination navigation, or message if no data.
        """
        if not self.data_length:
            return "暂无此信息!"
        
        page_links = [
            '<nav aria-label="Page navigation">',
            '<ul class="pagination">'
        ]
        
        # First page link
        self.get_data["page"] = 1
        page_links.append(
            f'<li><a href="?{self.get_data.urlencode()}" aria-label="Previous">'
            f'<span aria-hidden="true">首页</span></a></li>'
        )
        
        # Previous page link
        self.get_data["page"] = self.current_page - 1
        page_links.append(
            f'<li><a href="?{self.get_data.urlencode()}" aria-label="Previous">'
            f'<span aria-hidden="true">&laquo;</span></a></li>'
        )
        
        # Page number links
        for i in range(self.start_page_number, self.end_page_number):
            self.get_data["page"] = i
            css_class = 'class="active"' if i == self.current_page else ''
            page_links.append(
                f'<li {css_class}><a href="?{self.get_data.urlencode()}">{i}</a></li>'
            )
        
        # Next page link
        self.get_data["page"] = self.current_page + 1
        page_links.append(
            f'<li><a href="?{self.get_data.urlencode()}" aria-label="Next">'
            f'<span aria-hidden="true">&raquo;</span></a></li>'
        )
        
        # Last page link
        self.get_data["page"] = self.total_page_count
        page_links.append(
            f'<li><a href="?{self.get_data.urlencode()}" aria-label="Previous">'
            f'<span aria-hidden="true">尾页</span></a></li>'
        )
        
        page_links.extend(['</ul>', '</nav>'])
        
        return mark_safe('\n'.join(page_links))
