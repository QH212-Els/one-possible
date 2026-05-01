from japanese_reply_agent import JapaneseReplyAgentSystem
from consumer_law_agent import ConsumerLawAgentSystem
from work_shift_agent import WorkShiftAgentSystem


def show_menu():
    print("====================================")
    print(" 留学生生活サポート Multi-Agent System")
    print("====================================")
    print("请选择功能：")
    print("1. 日语消息回复 Agent")
    print("2. 消费法律小助手 Agent")
    print("3. 兼职排班与收入管理 Agent")
    print("q. 退出程序")
    print("------------------------------------")


def main():
    reply_system = JapaneseReplyAgentSystem()
    law_system = ConsumerLawAgentSystem()
    work_system = WorkShiftAgentSystem()

    while True:
        show_menu()
        choice = input("请输入选项：\n> ").strip()

        if choice.lower() == "q":
            print("程序已结束。")
            break

        elif choice == "1":
            print("\n【日语消息回复 Agent】")
            message = input("请输入你收到的日语消息：\n> ")
            user_intention = input("\n你想怎么回复？例如：确认时间、表示感谢、拒绝、道歉等。\n> ")

            result = reply_system.run(message, user_intention)

            print("\n========== 分析结果 ==========")
            print(f"【场景判断】{result['scene']}")
            print(f"【对方意图】{result['intention']}")
            print(f"【重要信息】{result['important_info']}")

            print("\n========== 回复生成 ==========")
            print("【简洁版】")
            print(result["reply_simple"])

            print("\n【礼貌版】")
            print(result["reply_polite"])

            print("\n【自然版】")
            print(result["reply_natural"])

            print("\n========== 检查结果 ==========")
            print(result["check_result"])
            print()

        elif choice == "2":
            print("\n【消费法律小助手 Agent】")
            problem = input("请简单输入你遇到的问题，例如：买了东西想退、被要求搬家、打工工资没发等。\n> ")

            result = law_system.run(problem)

            print("\n========== 判断结果 ==========")
            print(f"【问题类型】{result['category']}")
            print(f"【相关制度】{result['related_law']}")
            print(f"【风险程度】{result['risk_level']}")

            print("\n========== 简单说明 ==========")
            print(result["explanation"])

            print("\n========== 建议行动 ==========")
            print(result["action"])

            print("\n========== 注意 ==========")
            print(result["disclaimer"])
            print()

        elif choice == "3":
            print("\n【兼职排班与收入管理 Agent】")
            hourly_wage = input("请输入时薪（日元），例如 1200：\n> ")
            weekly_hours = input("请输入本周预计打工小时数，例如 20：\n> ")
            course_days = input("请输入本周上课时间说明，例如：周一周五15点下课，周三17点下课：\n> ")
            work_days = input("请输入本周排班说明，例如：周二18-22点，周六10-18点：\n> ")

            result = work_system.run(hourly_wage, weekly_hours, course_days, work_days)

            print("\n========== 计算结果 ==========")
            print(f"【预计周收入】{result['weekly_income']} 円")
            print(f"【预计月收入】{result['monthly_income']} 円")
            print(f"【每周工时判断】{result['hour_check']}")
            print(f"【课程冲突判断】{result['schedule_check']}")

            print("\n========== 建议 ==========")
            print(result["advice"])
            print()

        else:
            print("选项输入错误，请重新输入。\n")


if __name__ == "__main__":
    main()
