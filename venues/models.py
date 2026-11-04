from django.db import models


class Venue(models.Model):
    name = models.CharField(max_length=120)
    city = models.CharField(max_length=80)
    address = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Section(models.Model):
    venue = models.ForeignKey(
        Venue, on_delete=models.CASCADE, related_name="sections"
    )
    name = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["venue", "name"], name="unique_section_per_venue"
            )
        ]

    def __str__(self):
        return f"{self.venue.name} - {self.name}"


class Seat(models.Model):
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="seats"
    )
    row = models.PositiveIntegerField()
    number = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["section", "row", "number"], name="unique_seat_in_section"
            )
        ]

    def __str__(self):
        return f"{self.section.name}, rând {self.row}, loc {self.number}"
        