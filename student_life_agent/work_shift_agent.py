import re


class IncomeAgent:
    """
    收入计算 Agent
    作用：根据时薪和每周工时计算预计收入。
    """

    def calculate(self, hourly_wage: float, weekly_hours: float) -> dict:
        weekly_income = int(hourly_wage * weekly_hours)
        monthly_income = int(weekly_income * 4)
        return {
            "weekly_income": weekly_income,
            "monthly_income": monthly_income
        }


class WorkHourLimitAgent:
    """
    工时检查 Agent
    作用：检查是否接近或超过留学生常见的每周28小时打工限制。
    """

    def check(self, weekly_hours: float) -> str:
        if weekly_hours > 28:
            return "超过28小时，风险较高。留学生通常需要注意每周打工时间限制。"
        if weekly_hours >= 25:
            return "接近28小时，建议谨慎安排，避免超过限制。"
        return "目前没有超过28小时，看起来比较安全。"


class ScheduleConflictAgent:
    """
    课程冲突判断 Agent
    作用：根据简单关键词判断排班是否可能和课程冲突。
    这是基础版本，只做简单提示，不做复杂日历计算。
    """

    def check(self, course_days: str, work_days: str) -> str:
        possible_conflicts = []

        days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日",
                "月曜", "火曜", "水曜", "木曜", "金曜", "土曜", "日曜"]

        for day in days:
            if day in course_days and day in work_days:
                possible_conflicts.append(day)

        if possible_conflicts:
            return "可能有冲突的日期：" + "、".join(possible_conflicts) + "。请确认上课结束时间和出勤时间。"
        return "没有从文字中发现明显的课程和排班日期冲突。"


class AdviceAgent:
    """
    建议 Agent
    作用：根据工时和收入结果给出建议。
    """

    def suggest(self, weekly_hours: float, weekly_income: int, schedule_check: str) -> str:
        advice = []

        if weekly_hours > 28:
            advice.append("建议减少排班，先把每周工时控制在28小时以内。")
        elif weekly_hours >= 25:
            advice.append("工时已经比较接近上限，最好不要再临时加班。")
        else:
            advice.append("当前工时比较合理，可以继续注意学习和打工的平衡。")

        if weekly_income >= 35000:
            advice.append("本周收入较高，但也要注意不要因为打工影响上课和作业。")
        else:
            advice.append("收入计算结果可以作为生活费安排参考。")

        if "可能有冲突" in schedule_check:
            advice.append("建议把课程表和排班表再详细对照，必要时提前和店长说明。")

        return "\n".join(advice)


class InputConvertAgent:
    """
    输入转换 Agent
    作用：把用户输入的数字字符串转为 float。
    """

    def to_float(self, value: str, default: float = 0.0) -> float:
        numbers = re.findall(r"\d+(?:\.\d+)?", value)
        if not numbers:
            return default
        return float(numbers[0])


class WorkShiftAgentSystem:
    """
    兼职排班与收入管理总控制系统：
    InputConvertAgent → IncomeAgent → WorkHourLimitAgent → ScheduleConflictAgent → AdviceAgent
    """

    def __init__(self):
        self.convert_agent = InputConvertAgent()
        self.income_agent = IncomeAgent()
        self.limit_agent = WorkHourLimitAgent()
        self.conflict_agent = ScheduleConflictAgent()
        self.advice_agent = AdviceAgent()

    def run(self, hourly_wage_input: str, weekly_hours_input: str, course_days: str, work_days: str) -> dict:
        hourly_wage = self.convert_agent.to_float(hourly_wage_input)
        weekly_hours = self.convert_agent.to_float(weekly_hours_input)

        income = self.income_agent.calculate(hourly_wage, weekly_hours)
        hour_check = self.limit_agent.check(weekly_hours)
        schedule_check = self.conflict_agent.check(course_days, work_days)
        advice = self.advice_agent.suggest(weekly_hours, income["weekly_income"], schedule_check)

        return {
            "weekly_income": income["weekly_income"],
            "monthly_income": income["monthly_income"],
            "hour_check": hour_check,
            "schedule_check": schedule_check,
            "advice": advice
        }
