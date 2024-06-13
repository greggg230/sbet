from sbet.data.historical.extractor.odds_portal.models.odds_portal_page import OddsPortalPage
from sbet.data.historical.extractor.odds_portal.models.odds_portal_row import OddsPortalRow


def parse_odds_portal_json(json_data: dict) -> OddsPortalPage:
    page = json_data['d']['page']
    pageCount = json_data['d']['onePage']
    rows_data = json_data['d']['rows']

    rows = frozenset(
        OddsPortalRow(
            home_team=row['home-name'],
            away_team=row['away-name'],
            date_start_timestamp=row['date-start-timestamp'],
            home_score=int(row['homeResult']),
            away_score=int(row['awayResult']),
            home_moneyline_price=float(row['odds'][0]['avgOdds']),
            draw_moneyline_price=float(row['odds'][1]['avgOdds']),
            away_moneyline_price=float(row['odds'][2]['avgOdds']),
        )
        for row in rows_data
    )

    return OddsPortalPage(page=page, pageCount=pageCount, rows=rows)
