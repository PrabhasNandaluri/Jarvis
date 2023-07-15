import pandas as pd
import nsepython
from datetime import date, timedelta
import pandas_market_calendars as mcal
import yfinance as yf
import os
from util import send_mail


class PreMarketAnalysis:
    def __init__(self, Last_Working_Day) -> None:
        """This Class is Used when U need Create Report for Pre Market Analysis
        input : last woking day(date time)
        output : sned mail"""

        self.Last_working_day = (
            Last_Working_Day  # needs to get data of last working day
        )
        self.Markets_list: dict = {
            "S&P": "^SPX",
            "NASDAQ": "^NDX",
            "Dow": "^DJI",
            "Dollar Index": "DX-Y.NYB",
        }
        self.Premarket_template: str = (
            f"{os.getcwd()}\data\\templates\PreMarketAnalysis.html"
        )

    def Global_indices(self, ticker) -> pd.DataFrame:
        data = yf.download(ticker, start=self.Last_working_day, end=today)
        print(f"{ticker} \n {data}")
        return data

    def FII_Data(self) -> float:
        """Returns FII Long_percentage"""

        datestring: str = self.Last_working_day.strftime("%d%m%Y")
        URL: str = f"https://archives.nseindia.com/content/nsccl/fao_participant_oi_{datestring}.csv"
        data = pd.read_csv(URL)
        data = data.rename(columns=data.iloc[0]).drop(
            labels=0
        )  # Changing headers of pandas dataframe
        long_percentage: float = (
            int(data["Future Index Long"][3])
            / (int(data["Future Index Long"][3]) + int(data["Future Index Short"][3]))
        ) * 100

        return long_percentage

    def Run(self) -> None:
        with open(self.Premarket_template, "r+") as f:
            template = f.read()
            HTML = template.replace("Long_Percentage", str(PMA.FII_Data()))
            for market in self.Markets_list:
                hloc_values = self.Global_indices(self.Markets_list[market])
                try:
                    HTML = HTML.replace(
                        f"<{self.Markets_list[market]}>",
                        f"<tr><td>{market}</td><td>{hloc_values.iloc[0][0]}</td><td>{hloc_values.iloc[0][1]}</td><td>{hloc_values.iloc[0][2]}</td><td>{hloc_values.iloc[0][3]}</td></tr>",
                    )

                except Exception:
                    print("error oeccured while processing for market")
            try:
                f = open("myfile.html", "x")
            except FileExistsError:
                f = open("myfile.html", "w")
            finally:
                f.write(HTML)
                f.close()
        subject = f"Premarket Analysis {date.today()}"
        send_mail(subject, HTML, "prabhasreddy030@gmail.com")


if __name__ == "__main__":
    # Getting the last working day's date
    today = date.today()
    nse = mcal.get_calendar("NSE")
    schedule = nse.schedule(start_date=today - timedelta(days=365), end_date=today)
    last_working_day = schedule.iloc[-1].name
    if last_working_day == pd.Timestamp(today):
        last_working_day = schedule.iloc[-2].name

    PMA = PreMarketAnalysis(last_working_day)
    PMA.Run()
