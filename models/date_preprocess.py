import pandas as pd
from datetime import datetime, time, date, timedelta
from models.global_vars import *
from models.global_vars import GlobalVar
from utils.utils import datetime_from_string


def prepare_df(attend_df, salary_df, shifts_df):
    attend_df.rename(columns={'الشركة': 'Company', 'الرقم': 'Number', 'الاسم': 'Name'
        , 'القسم': 'Section', 'الوظيفة': 'Job', "الوردية": 'Shift'
        , 'التاريخ': 'Date', 'اليوم': 'Day', 'دوام اليوم': 'Attendance'
        , 'دخول': 'Check-in', 'خروج': 'Check-out', 'ساعات حضور': 'Attended-hours'
        , 'التأخر': 'lateness', 'نوع التأخر': 'Lateness type', 'خروج مبكر': 'Early Check-out'
        , 'نوع الخروج المبكر': 'Early Check-out Type', 'إجازة ساعية': 'Hourly Leave', 'الإضافي المبكر': 'Early Check-in'
        , 'إضافي أول': 'Late Check-out', 'إضافي العطل': 'Vacation extra', 'ملاحظات': 'Note'
                              }, inplace=True)
    attend_df = attend_df.merge(salary_df, left_on="Name", right_on="Name")
    attend_df = attend_df.merge(shifts_df, left_on="Shift", right_on="Shift Name")
    attend_df['Attendance'] = attend_df['Attendance'].replace('حضور', 'working')
    attend_df["Attendance"] = attend_df["Attendance"].str.replace('عطلة أسبوعية', 'vacation', regex=False)
    attend_df["Attendance"] = attend_df["Attendance"].str.replace('عطلة رسمية', 'official_vacation', regex=False)
    attend_df["Attendance"] = attend_df["Attendance"].str.replace('إجازة بلا راتب', 'unpaid_vacation', regex=False)
    attend_df["Attendance"] = attend_df["Attendance"].str.replace('مهمة خارجية', 'paid_outsource', regex=False)
    attend_df["Attendance"] = attend_df["Attendance"].str.replace('غياب غير مبرر', 'Unjustified', regex=False)
    attend_df["Attendance"] = attend_df["Attendance"].str.replace('إجازة إدارية', 'paid_vacation', regex=False)
    attend_df["Day"] = attend_df["Day"].str.replace('الخميس', 'thu', regex=False)
    attend_df["Day"] = attend_df["Day"].str.replace('الجمعة', 'fri', regex=False)
    attend_df["Day"] = attend_df["Day"].str.replace('السبت', 'sat', regex=False)
    attend_df["Day"] = attend_df["Day"].str.replace('الأحد', 'sun', regex=False)
    attend_df["Day"] = attend_df["Day"].str.replace('الإثنين', 'mon', regex=False)
    attend_df["Day"] = attend_df["Day"].str.replace('الثلاثاء', 'tue', regex=False)
    attend_df["Day"] = attend_df["Day"].str.replace('الأربعاء', 'wed', regex=False)
    attend_df["Early Check-out Type"] = attend_df["Early Check-out Type"].fillna('')
    attend_df["Early Check-out Type"] = attend_df["Early Check-out Type"].str.replace('غير مبرر', 'Unjustified',
                                                                                      regex=False)
    attend_df["Early Check-out Type"] = attend_df["Early Check-out Type"].str.replace('مبرر', 'Justified', regex=False)
    attend_df["Early Check-out Type"] = attend_df["Early Check-out Type"].str.replace('إجازة ساعية بلا راتب', 'Unpaid',
                                                                                      regex=False)
    attend_df["Early Check-out Type"] = attend_df["Early Check-out Type"].str.replace('إجازة ساعية', 'Paid',
                                                                                      regex=False)
    attend_df["Lateness type"] = attend_df["Lateness type"].str.replace('غير مبرر', 'Unjustified', regex=False)
    attend_df["Lateness type"] = attend_df["Lateness type"].str.replace('مبرر', 'Justified', regex=False)
    attend_df["Check-in"] = attend_df["Check-in"].str.replace('nan', '0', regex=False)
    attend_df[['Check-in', 'Check-out']] = attend_df[['Check-in', 'Check-out']].fillna('00:00')
    attend_df['Early Check-in'] = attend_df['Early Check-in'].astype('string')
    attend_df['Hourly Leave'] = attend_df['Hourly Leave'].astype('string')
    attend_df.loc[attend_df['Attended-hours'].isin([0]), 'Attended-hours'] = '00:00'
    attend_df.loc[attend_df['Attended-hours'].isin(["0"]), 'Attended-hours'] = '00:00'
    attend_df['Attended-hours'] = pd.to_datetime(attend_df['Attended-hours'], format='%H:%M')
    attend_df['Shift-Check-in'] = pd.to_datetime(attend_df['Shift-Check-in'], format='%H:%M')
    attend_df['Shift-Check-out'] = pd.to_datetime(attend_df['Shift-Check-out'], format='%H:%M')
    attend_df = attend_df.drop(columns=['Company', 'Section', 'Job', 'Note', 'Finger Print Number', 'Unnamed: 0',
                                        'Grace Period', 'per minute deduction', 'Doubled Deduction'])
    attend_df['index'] = range(1, len(attend_df) + 1)

    return attend_df


def attend_calc(df):
    df["correct_check_in"] = 0
    df["correct_check_out"] = 0
    df["work_hours"] = timedelta(hours=0)  # datetime(1900, 1, 1, 0, 0, 0)
    df["deduct_hours"] = timedelta(hours=0)
    df["vacation_extra"] = 0
    df["Check_early_extra"] = False
    df["early_extra"] = None
    df["Check_late_extra"] = False
    df["late_extra"] = None
    # df.loc[df['Early Check-out'].isin(['0']), 'Early Check-out'] = '00:00'
    # df['Early Check-out'] = pd.to_datetime(df['Early Check-out'], format='%H:%M')

    for idx, item in df.iterrows():
        if df["Attendance"][idx] == "working":
            # .  Check in
            # . Early
            if item["Check-in2"] < item["Shift-Check-in"] - timedelta(minutes=30):
                df.loc[idx, "correct_check_in"] = 2
            elif item["Check-in2"] < item["Shift-Check-in"]:
                df.loc[idx, "correct_check_in"] = 1
                # . Late
            else:
                if item["Check-in2"] > item["Shift-Check-in"] + timedelta(minutes=30):
                    df.loc[idx, "correct_check_in"] = -2
                else:
                    df.loc[idx, "correct_check_in"] = -1
                    # .   Check out
            # .     Extra
            if item["Check-out2"] > item["Shift-Check-out"] + timedelta(minutes=30):
                df.loc[idx, "correct_check_out"] = 2
            elif item["Check-out2"] > item["Shift-Check-out"]:
                df.loc[idx, "correct_check_out"] = 1
            # .  Early
            else:
                df.loc[idx, "correct_check_out"] = -1
                # . End
        else:
            pass
        # after edit
        # .  Correct checks
        # print("attend hours", df["Attended-hours"][idx])
        if df["Shift Name"][idx] == "Part_Time":
            df.loc[idx, "work_hours"] += df["Check-out2"][idx] - df["Check-in2"][idx]
        else:
            if df["correct_check_in"][idx] == 1 and df["correct_check_out"][idx] == 1 and df["Attendance"][
                idx] == "working":
                df.loc[idx, "work_hours"] += timedelta(hours=df["Shift-hours"][idx])

                # print("Get 8 hours 1")
            # .  Paid Vacation or out source

            elif df["Attendance"][idx] == "paid_outsource" or df["Attendance"][idx] == "official_vacation"\
                    or df["Attendance"][idx] == "paid_vacation":
                df.loc[idx, "work_hours"] += timedelta(hours=df["Shift-hours"][idx])

                # print("Get 8 hours 2")

            # . Vacation and not a part timer
            elif df["Attendance"][idx] == "vacation" and df["Shift"][idx] != "Part-time":
                df.loc[idx, "work_hours"] += timedelta(hours=df["Shift-hours"][idx])
                # print("Get 8 hours 3")


            # .  Correct check in \\ Not correct check out
            elif df["correct_check_in"][idx] == 1 and df["correct_check_out"][idx] != 1:
                df.loc[idx, "work_hours"] += timedelta(hours=df["Shift-hours"][idx])
                if df["correct_check_out"][idx] == 2:
                    # print("HI EXTRA Need to aprove ")
                    # df.loc[idx, "Check_late_extra"]= True
                    df.loc[idx, "late_extra"] = df["Check-out2"][idx] - df["Shift-Check-out"][idx]
                else:  # Early check out
                    if item["Early Check-out Type"] in GlobalVar.justified:
                        if df["Check-out2"][idx] - df["Check-in2"][idx] > df["Early Check-out"][idx]:
                            df.loc[idx, "work_hours"] -= df["Shift-Check-out"][idx] - df["Check-out2"][idx] - \
                                                         df["Early Check-out"][idx]
                            df.loc[idx, "deduct_hours"] += df["Shift-Check-out"][idx] - df["Check-out2"][idx] - \
                                                           df["Early Check-out"][idx]
                    else:
                        if item["Early Check-out Type"] == "unpaid":
                            df.loc[idx, "work_hours"] -= (df["Shift-Check-out"][idx] - df["Check-out2"][idx])
                            df.loc[idx, "deduct_hours"] += (df["Shift-Check-out"][idx] - df["Check-out2"][idx])
                        else:
                            df.loc[idx, "work_hours"] -= (df["Shift-Check-out"][idx] - df["Check-out2"][idx]) * 2
                            df.loc[idx, "deduct_hours"] += (df["Shift-Check-out"][idx] - df["Check-out2"][idx]) * 2



            # .  Not Correct check in \\ Correct check out
            elif df["correct_check_in"][idx] != 1 and df["correct_check_out"][idx] == 1:
                df.loc[idx, "work_hours"] += timedelta(hours=df["Shift-hours"][idx])
                if df["correct_check_in"][idx] == 2:
                    # df.loc[idx, "Check_early_extra"] = True
                    df.loc[idx, "early_extra"] = df["Shift-Check-in"][idx] - df["Check-in2"][idx]
                elif df["correct_check_in"][idx] == -1:
                    shift_time = df['Shift-Check-out'][idx] - df['Shift-Check-in'][idx] - timedelta(minutes=9)
                    attend_time = item["Check-out2"] - item["Check-in2"]
                    if attend_time < shift_time:
                        if df["Lateness type"][idx] in GlobalVar.unjustified:
                            df.loc[idx, "work_hours"] -= (df["Check-in2"][idx] - df["Shift-Check-in"][idx])
                            df.loc[idx, "deduct_hours"] += (df["Check-in2"][idx] - df["Shift-Check-in"][idx])

                        else:
                            pass
                            # print("why late??   Justified")
                else:
                    if df["Lateness type"][idx] in GlobalVar.unjustified:
                        df.loc[idx, "work_hours"] -= (df["Check-in2"][idx] - df["Shift-Check-in"][idx]) * 2
                        df.loc[idx, "deduct_hours"] += (df["Check-in2"][idx] - df["Shift-Check-in"][idx]) * 2
                    elif df["Lateness type"][idx] == "unpaid":
                        df.loc[idx, "work_hours"] -= (df["Check-in2"][idx] - df["Shift-Check-in"][idx])
                        df.loc[idx, "deduct_hours"] += (df["Check-in2"][idx] - df["Shift-Check-in"][idx])
                    else:
                        pass
                        # print("why late??   Justified")
                # print("just  2")


            # .  Not Correct check in \\ Not Correct check out
            elif df["correct_check_in"][idx] != 1 and df["correct_check_out"][idx] != 1:
                # df["work_hours"][idx] += timedelta(hours=8)
                df.loc[idx, "work_hours"] += timedelta(hours=df["Shift-hours"][idx])

                if df["correct_check_in"][idx] == -2:
                    if df["Lateness type"][idx] in GlobalVar.unjustified:
                        df.loc[idx, "work_hours"] -= (df["Check-in2"][idx] - df["Shift-Check-in"][idx]) * 2
                        df.loc[idx, "deduct_hours"] += (df["Check-in2"][idx] - df["Shift-Check-in"][idx]) * 2
                    elif df["Lateness type"][idx] == "unpaid" :
                        df.loc[idx, "work_hours"] -= (df["Check-in2"][idx] - df["Shift-Check-in"][idx])
                        df.loc[idx, "deduct_hours"] += (df["Check-in2"][idx] - df["Shift-Check-in"][idx])

                    if df["correct_check_out"][idx] == -1:
                        if item["Early Check-out Type"] in GlobalVar.justified:
                            if df["Check-out2"][idx] - df["Check-in2"][idx] > df["Early Check-out"][idx]:
                                df.loc[idx, "work_hours"] -= df["Shift-Check-out"][idx] - df["Check-out2"][idx] - \
                                                             df["Early Check-out"][idx]
                                df.loc[idx, "deduct_hours"] += df["Shift-Check-out"][idx] - df["Check-out2"][idx] - \
                                                               df["Early Check-out"][idx]
                        elif item["Early Check-out Type"] == "unpaid":
                            df.loc[idx, "work_hours"] -= (df["Shift-Check-out"][idx] - df["Check-out2"][idx])
                            df.loc[idx, "deduct_hours"] += (df["Shift-Check-out"][idx] - df["Check-out2"][idx])
                        else:
                            df.loc[idx, "work_hours"] -= (df["Shift-Check-out"][idx] - df["Check-out2"][idx]) * 2
                            df.loc[idx, "deduct_hours"] += (df["Shift-Check-out"][idx] - df["Check-out2"][idx]) * 2
                        # print("Came too late and leave late")
                    else:
                        # df.loc[idx, "Check_late_extra"]= True
                        df.loc[idx, "late_extra"] = df["Check-out2"][idx] - df["Shift-Check-out"][idx]
                        # print("Came too late and leave with extra")



                elif df["correct_check_in"][idx] == 2:
                    # df.loc[idx, "Check_early_extra"] = True
                    df.loc[idx, "early_extra"] = df["Shift-Check-in"][idx] - df["Check-in2"][idx]
                    if df["correct_check_out"][idx] == 2:
                        # df.loc[idx, "Check_late_extra"]= True
                        df.loc[idx, "late_extra"] = df["Check-out2"][idx] - df["Shift-Check-out"][idx]
                        # print("Came extra and leave extra ")
                    else:
                        if item["Early Check-out Type"] in GlobalVar.justified:
                            if df["Check-out2"][idx] - df["Check-in2"][idx] > df["Early Check-out"][idx]:
                                df.loc[idx, "work_hours"] -= df["Shift-Check-out"][idx] - df["Check-out2"][idx] - \
                                                             df["Early Check-out"][idx]
                                df.loc[idx, "deduct_hours"] += df["Shift-Check-out"][idx] - df["Check-out2"][idx] - \
                                                               df["Early Check-out"][idx]
                        elif item["Early Check-out Type"] == "unpaid":
                            df.loc[idx, "work_hours"] -= (df["Shift-Check-out"][idx] - df["Check-out2"][idx])
                            df.loc[idx, "deduct_hours"] += (df["Shift-Check-out"][idx] - df["Check-out2"][idx])

                        else:
                            df.loc[idx, "work_hours"] -= (df["Shift-Check-out"][idx] - df["Check-out2"][idx]) * 2
                            df.loc[idx, "deduct_hours"] += (df["Shift-Check-out"][idx] - df["Check-out2"][idx]) * 2
                        # print("Came extra and leave early ")



                else:  # df["correct_check_in"][idx] == -1
                    if df["correct_check_out"][idx] == 2:
                        # df.loc[idx, "Check_late_extra"]= True
                        df.loc[idx, "late_extra"] = df["Check-out2"][idx] - df["Shift-Check-out"][idx]
                        # print("Came late and have extra ")
                    else:

                        if df["Lateness type"][idx] in GlobalVar.unjustified:
                            df.loc[idx, "work_hours"] -= df["Check-in2"][idx] - df["Shift-Check-in"][idx]
                            df.loc[idx, "deduct_hours"] += df["Check-in2"][idx] - df["Shift-Check-in"][idx]
                        elif df["Lateness type"][idx] == "unpaid":
                            df.loc[idx, "work_hours"] -= df["Check-in2"][idx] - df["Shift-Check-in"][idx]
                            df.loc[idx, "deduct_hours"] += df["Check-in2"][idx] - df["Shift-Check-in"][idx]
                        if item["Early Check-out Type"] in GlobalVar.justified:
                            if df["Check-out2"][idx] - df["Check-in2"][idx] > df["Early Check-out"][idx]:
                                df.loc[idx, "work_hours"] -= df["Shift-Check-out"][idx] - df["Check-out2"][idx] - \
                                                             df["Early Check-out"][idx]
                                df.loc[idx, "deduct_hours"] += df["Shift-Check-out"][idx] - df["Check-out2"][idx] - \
                                                               df["Early Check-out"][idx]
                        elif item["Early Check-out Type"] == "unpaid":
                            df.loc[idx, "work_hours"] -= (df["Shift-Check-out"][idx] - df["Check-out2"][idx])
                            df.loc[idx, "deduct_hours"] += (df["Shift-Check-out"][idx] - df["Check-out2"][idx])

                        else:
                            df.loc[idx, "work_hours"] -= (df["Shift-Check-out"][idx] - df["Check-out2"][idx]) * 2
                            df.loc[idx, "deduct_hours"] += (df["Shift-Check-out"][idx] - df["Check-out2"][idx]) * 2
                    # print("Came late and leave early ")
        # if df['work_hours'][idx] < timedelta(hours=0):
        #     df.loc[idx,"deduct_hours"] -= df['work_hours'][idx]
        # else:
        if df["Attendance"][idx] == "vacation" and df["Attended-hours"][idx] != pd.Timestamp('1900-01-01 00:00:00'):
            print("get extra on vacation?", df["Attended-hours"][idx])
        # print(df["work_hours"][idx].time())
        # print("----------------------------------------")

    # df["work_hours"] = df["work_hours"].apply(lambda x: x.time())
    # df["deduct_hours"] = df["deduct_hours"].apply(lambda x: x.time())

    return df
