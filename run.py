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

    # check_in_date = input('Enter check_in_date\n')
    # check_out_date = input('Enter check_out_date\n')

    bot.select_dates('2025-04-24', '2025-04-27')
    # bot.select_dates(check_in_date, check_out_date)
    # adults_count = int(input('Enter adults_count\n'))
    bot.select_adults(4)

    # bot.select_adults(adults_count)
    bot.click_search()
    # filter = input('filter results! (asc, dsc, none)')
    bot.apply_filtrations('none')
    bot.refresh()
    bot.report_results()