# Generated by Django 3.2.19 on 2023-08-17 21:21

from django.db import migrations


def migrate_phase_funding(apps, schema_editor):
    PortfolioPhase = apps.get_model('asset_dashboard', 'PortfolioPhase')
    portfolio_phases = PortfolioPhase.objects.all()

    for p in portfolio_phases:
        fundings = p.phase.funding_streams.all()
        for index, funding in enumerate(fundings):
            if index == 0:
                p.phase_funding_stream = funding
                p.save()
            else:
                new_portfolio_phase = PortfolioPhase.objects.create(
                    phase=p.phase,
                    portfolio=p.portfolio,
                    sequence=p.sequence,
                    phase_funding_stream=funding
                )

class Migration(migrations.Migration):

    dependencies = [
        ('asset_dashboard', '0044_portfoliophase_phase_funding_stream'),
    ]

    operations = [
        migrations.RunPython(migrate_phase_funding),
    ]