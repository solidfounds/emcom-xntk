from django.contrib import admin
from .models import Orden, OrderItem
import csv
import datetime
from django.http import HttpResponse
from django.core.urlresolvers import reverse

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    #escribe tu primera tabla con header informacion
    writer.writerow([ field.verbose_name for field in fields])
    #write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):

    def order_detail(obj):
        return '<a href="{}">View</a>'.format(
            reverse('orders:admin_order_detail', args=[obj.id]))
    order_detail.allow_tags = True

    def order_pdf(obj):
        return '<a href="{}">PDF</a>'.format(
            reverse('orders:admin_order_pdf', args=[obj.id]))
    order_pdf.allow_tags = True
    order_pdf.short_description = 'PDF bill'


    actions = [export_to_csv]
    list_display = ['id','nombre', 'apellidos', 'email', 'direccion', 'codigo_postal' ,
                    'ciudad', 'creado', 'actualizado', 'pagado',order_detail,]
    list_filter = ['pagado', 'creado', 'actualizado']
    inlines = [OrderItemInline]

