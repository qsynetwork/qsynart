from django.contrib import admin
from mainwebsite.models import *
from django.utils.html import format_html


class ArtistsAdmin(admin.ModelAdmin):
    def artworks(self):
        html = ""
        for i in self.artwork_of_artist.all():
            html += f"<a href=\"/admin/mainwebsite/artwork/{i.id}/change/\" target=\"__blank\">Picture Id {i.id}</a><br>"
        return  format_html(html)
    artworks.allow_tags = True
    list_display = ["name",artworks]
    search_fields = ["name"]


admin.site.register(Artists, ArtistsAdmin)

admin.site.register(Artwork)
admin.site.register(ArtworkSize)
admin.site.register(OrderHistory)
