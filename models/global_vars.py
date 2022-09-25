from datetime import datetime, date, time

import pandas as pd


class GlobalVar:
    attendance_df = pd.DataFrame()
    salary_df = pd.DataFrame()
    shifts_df = pd.DataFrame()
    final_df = pd.DataFrame()
    justified = ["Justified", "justified", "Justify", "justify", "yes", "y", "true", "t", "Paid Leave", "paid leave",
                 "ok"]
    unjustified = ["Unjustified", "unjustified", "Unjustify", "unjustify", "no", "n", "false", "f"]
