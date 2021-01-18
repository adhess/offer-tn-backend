from rest_framework import filters


class M2MFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        """
        Filters a queryset using a list of comma separated primary key values
        """

        value_list = request.query_params.get('pk')
        if value_list:
            value_list = value_list.split(',')
            return queryset.filter(pk__in=value_list)
        return queryset

