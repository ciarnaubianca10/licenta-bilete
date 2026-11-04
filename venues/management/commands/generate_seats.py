from django.core.management.base import BaseCommand, CommandError

from venues.models import Section, Seat


class Command(BaseCommand):
    help = "Generează automat locurile unui sector (rânduri x locuri pe rând)"

    def add_arguments(self, parser):
        parser.add_argument("section_id", type=int)
        parser.add_argument("rows", type=int)
        parser.add_argument("seats_per_row", type=int)

    def handle(self, *args, **options):
        try:
            section = Section.objects.get(pk=options["section_id"])
        except Section.DoesNotExist:
            raise CommandError("Sectorul cu acest ID nu există.")

        seats = [
            Seat(section=section, row=row, number=number)
            for row in range(1, options["rows"] + 1)
            for number in range(1, options["seats_per_row"] + 1)
        ]

        Seat.objects.bulk_create(seats, ignore_conflicts=True)

        total = section.seats.count()
        self.stdout.write(
            self.style.SUCCESS(f"{section} are acum {total} locuri.")
        )