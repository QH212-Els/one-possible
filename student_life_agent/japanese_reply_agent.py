import re


class SceneAgent:
    """
    场景判断 Agent
    作用：判断收到的日语消息属于什么场景。
    """

    def analyze(self, message: str) -> str:
        if any(word in message for word in ["面接", "応募", "履歴書", "採用"]):
            return "兼职或面试相关"
        elif any(word in message for word in ["授業", "課題", "提出", "先生", "レポート"]):
            return "学校或课程相关"
        elif any(word in message for word in ["勤務", "シフト", "出勤", "休憩", "店長"]):
            return "打工排班相关"
        elif any(word in message for word in ["家賃", "契約", "退去", "部屋", "不動産"]):
            return "租房或生活手续相关"
        elif any(word in message for word in ["荷物", "配達", "再配達", "住所"]):
            return "快递或生活通知相关"
        else:
            return "一般日常沟通"


class IntentionAgent:
    """
    意图理解 Agent
    作用：判断对方希望用户做什么。
    """

    def analyze(self, message: str) -> str:
        if any(word in message for word in ["ご確認", "確認", "返事", "返信"]):
            return "对方希望你确认并回复"
        elif any(word in message for word in ["来てください", "お越しください", "お待ちしております"]):
            return "对方希望你按时间前往"
        elif any(word in message for word in ["提出してください", "送ってください"]):
            return "对方希望你提交或发送资料"
        elif any(word in message for word in ["可能ですか", "できますか", "よろしいでしょうか"]):
            return "对方在询问你的时间或是否方便"
        elif any(word in message for word in ["申し訳", "すみません"]):
            return "对方在说明情况或表达歉意"
        else:
            return "需要根据上下文进行普通回复"


class InformationAgent:
    """
    信息提取 Agent
    作用：提取时间、地点、需要携带的东西等重要信息。
    """

    def extract(self, message: str) -> str:
        infos = []

        time_patterns = [
            r"\d{1,2}時",
            r"\d{1,2}:\d{2}",
            r"午前\d{1,2}時",
            r"午後\d{1,2}時",
            r"明日",
            r"本日",
            r"今日",
            r"来週",
            r"今週"
        ]

        for pattern in time_patterns:
            infos.extend(re.findall(pattern, message))

        for item in ["履歴書", "身分証", "印鑑", "住所", "電話"]:
            if item in message:
                infos.append(item)

        if infos:
            return "、".join(sorted(set(infos)))
        return "没有明显的时间、地点或携带物信息"


class ReplyAgent:
    """
    回复生成 Agent
    作用：根据场景、意图和用户想法生成不同语气的日语回复。
    """

    def generate(self, scene: str, intention: str, user_intention: str) -> dict:
        return {
            "reply_simple": self._generate_simple(user_intention),
            "reply_polite": self._generate_polite(user_intention),
            "reply_natural": self._generate_natural(scene, user_intention)
        }

    def _generate_simple(self, user_intention: str) -> str:
        if "确认" in user_intention or "行ける" in user_intention or "可以" in user_intention:
            return "はい、承知しました。よろしくお願いいたします。"
        if "感谢" in user_intention or "ありがとう" in user_intention:
            return "ご連絡ありがとうございます。よろしくお願いいたします。"
        if "道歉" in user_intention or "遅れ" in user_intention:
            return "申し訳ございません。確認が遅くなりました。"
        if "拒绝" in user_intention or "無理" in user_intention or "不行" in user_intention:
            return "申し訳ございませんが、その時間は難しいです。"
        return "ご連絡ありがとうございます。確認いたしました。よろしくお願いいたします。"

    def _generate_polite(self, user_intention: str) -> str:
        if "确认" in user_intention or "可以" in user_intention:
            return (
                "お世話になっております。\n"
                "ご連絡ありがとうございます。\n"
                "内容を確認いたしました。\n"
                "当日はどうぞよろしくお願いいたします。"
            )
        if "感谢" in user_intention:
            return (
                "お世話になっております。\n"
                "ご丁寧にご連絡いただき、ありがとうございます。\n"
                "確認いたしました。\n"
                "引き続きよろしくお願いいたします。"
            )
        if "道歉" in user_intention:
            return (
                "お世話になっております。\n"
                "ご返信が遅くなり、大変申し訳ございません。\n"
                "内容を確認いたしました。\n"
                "何卒よろしくお願いいたします。"
            )
        if "拒绝" in user_intention or "不行" in user_intention:
            return (
                "お世話になっております。\n"
                "ご連絡ありがとうございます。\n"
                "大変申し訳ございませんが、その時間は都合が合わず伺うことが難しいです。\n"
                "別の時間でご調整いただくことは可能でしょうか。\n"
                "よろしくお願いいたします。"
            )
        return (
            "お世話になっております。\n"
            "ご連絡ありがとうございます。\n"
            "内容を確認いたしました。\n"
            "よろしくお願いいたします。"
        )

    def _generate_natural(self, scene: str, user_intention: str) -> str:
        if scene == "兼职或面试相关" and ("确认" in user_intention or "可以" in user_intention):
            return (
                "お世話になっております。\n"
                "ご連絡ありがとうございます。\n"
                "面接日時について承知いたしました。\n"
                "当日はよろしくお願いいたします。"
            )
        if scene == "打工排班相关" and ("确认" in user_intention or "可以" in user_intention):
            return (
                "お疲れ様です。\n"
                "ご連絡ありがとうございます。\n"
                "シフトの件、確認しました。\n"
                "よろしくお願いいたします。"
            )
        if scene == "学校或课程相关":
            return (
                "先生、お世話になっております。\n"
                "ご連絡ありがとうございます。\n"
                "内容を確認いたしました。\n"
                "よろしくお願いいたします。"
            )
        return (
            "ご連絡ありがとうございます。\n"
            "内容を確認しました。\n"
            "よろしくお願いいたします。"
        )


class CheckAgent:
    """
    检查 Agent
    作用：检查回复是否基本礼貌、是否过短、是否可能遗漏信息。
    """

    def check(self, reply: str, important_info: str) -> str:
        comments = []

        if "ありがとうございます" not in reply and "申し訳" not in reply:
            comments.append("回复中可以加入感谢或道歉表达，使语气更自然。")
        if "よろしくお願いいたします" not in reply:
            comments.append("建议结尾加入「よろしくお願いいたします」。")
        if len(reply) < 15:
            comments.append("回复稍微有点短，正式场合可以写得更完整。")
        if important_info != "没有明显的时间、地点或携带物信息":
            comments.append(f"注意确认消息中的重要信息：{important_info}")

        if not comments:
            return "回复整体比较自然，敬语和语气基本合适。"
        return "\n".join(comments)


class JapaneseReplyAgentSystem:
    """
    日语回复总控制系统：
    SceneAgent → IntentionAgent → InformationAgent → ReplyAgent → CheckAgent
    """

    def __init__(self):
        self.scene_agent = SceneAgent()
        self.intention_agent = IntentionAgent()
        self.info_agent = InformationAgent()
        self.reply_agent = ReplyAgent()
        self.check_agent = CheckAgent()

    def run(self, message: str, user_intention: str) -> dict:
        scene = self.scene_agent.analyze(message)
        intention = self.intention_agent.analyze(message)
        important_info = self.info_agent.extract(message)
        replies = self.reply_agent.generate(scene, intention, user_intention)
        check_result = self.check_agent.check(replies["reply_polite"], important_info)

        return {
            "scene": scene,
            "intention": intention,
            "important_info": important_info,
            "reply_simple": replies["reply_simple"],
            "reply_polite": replies["reply_polite"],
            "reply_natural": replies["reply_natural"],
            "check_result": check_result
        }
