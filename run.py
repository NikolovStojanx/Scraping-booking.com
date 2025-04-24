import time

from bot.booking.booking import Booking

with Booking() as bot:
    bot.land_first_page()
    # bot.change_currency("EUR")
    for _ in range(5):
        try:
            bot.select_place_to_go('Ohrid')

            break
        except Exception as e:
            print(e)

    bot.select_dates('2025-04-24', '2025-04-27')

    bot.select_adults(4)

    bot.click_search()

    # bot.apply_filtrations()
    # bot.refresh()
    bot.report_results()