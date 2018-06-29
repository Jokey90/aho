from django.contrib import admin
from main.models import *
from td.models import *
from mobile.models import *
from service.models import *

#     main app   -----------------------------------------------


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'department', 'group')
    search_fields = ['last_name', 'first_name', 'middle_name', 'department']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment')
    search_fields = ['name']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(GlobalSettings)
class GlobalSettingsAdmin(admin.ModelAdmin):
    list_display = ('key', 'name', 'value')


#  TD app ------------------------------------------------------


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'ownership_type')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('type', 'number', 'car', 'active')


@admin.register(ItemTracking)
class ItemTrackingAdmin(admin.ModelAdmin):
    list_display = ('item', 'date', 'added_by')


@admin.register(ProxyTracking)
class ProxyTrackingAdmin(admin.ModelAdmin):
    list_display = ('proxy', 'date', 'added_by')


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('emp', 'comment', 'license', 'phone', 'active')


@admin.register(BudgetItem)
class BudgetItemAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(BudgetSubitem)
class BudgetSubitemAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_item')


@admin.register(BudgetValue)
class BudgetValueAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'car', 'budget_subitem', 'amount')


@admin.register(Proxy)
class ProxyAdmin(admin.ModelAdmin):
    list_display = ('driver', 'car', 'type', 'start_date', 'end_date')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'car', 'driver', 'budget_subitem', 'amount')


@admin.register(Mileage)
class MileageAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'car', 'value')


@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ('number', 'car_name', 'owner', 'payment_type', 'contract')


@admin.register(Penalty)
class PenaltyAdmin(admin.ModelAdmin):
    list_display = ('car', 'number', 'date', 'description', 'amount')


@admin.register(VisitorsParking)
class VisitorsParkingAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'car_number', 'visitors_name', 'invited_by')


@admin.register(TO)
class TOAdmin(admin.ModelAdmin):
    list_display = ('date', 'car', 'name', 'budget_amount', 'fact_amount', 'mileage')


#  Mobile app ---------------------------------------------------


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('period', 'sim', 'number', 'amount')
    list_display_links = ('period', 'amount')


@admin.register(BillFile)
class BillFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'year', 'month')
    list_display_links = ('file',)


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('year', 'division', 'amount')
    list_display_links = ('amount',)


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'group', 'mts', 'active')
    list_display_links = ('number',)


@admin.register(Limit)
class LimitAdmin(admin.ModelAdmin):
    list_display = ('sim', 'amount', 'infinite', 'date')
    list_display_links = ('amount',)


@admin.register(Sim)
class SimAdmin(admin.ModelAdmin):
    list_display = ('number', 'tariff', 'active', 'current_owner', 'current_limit')
    list_display_links = ('number',)


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'active')
    list_display_links = ('name',)


@admin.register(Transition)
class TransitionAdmin(admin.ModelAdmin):
    list_display = ('date', 'sim', 'employee', 'comment')
    list_display_links = ('date',)


# --------------service app----------------------------------------------------------


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact')
    list_display_links = ('name',)


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'block', 'ord_number')
    list_display_links = ('name',)


@admin.register(ChecklistRow)
class ChecklistRowAdmin(admin.ModelAdmin):
    list_display = ('name', 'zone', 'ord_number')
    list_display_links = ('name', )


@admin.register(ChecklistValue)
class ChecklistValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'checklist', 'row', 'has_issues', 'solve_date')
    list_display_links = ('id', )


@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'floor')
    list_display_links = ('id', )


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'provider', 'issue', 'mail_sent', 'close_date')
