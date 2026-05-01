class LawCategoryAgent:
    """
    法律问题分类 Agent
    作用：判断用户的问题大概属于哪一类。
    """

    def analyze(self, problem: str) -> str:
        if any(word in problem for word in ["退货", "返品", "取消", "キャンセル", "网购", "ネット", "商品"]):
            return "购物、退货或取消相关"
        if any(word in problem for word in ["クーリング", "推销", "访问销售", "訪問販売", "电话销售", "電話勧誘"]):
            return "クーリング・オフ相关"
        if any(word in problem for word in ["租房", "家賃", "退去", "房东", "不動産", "契約"]):
            return "租房或合同相关"
        if any(word in problem for word in ["打工", "アルバイト", "工资", "給料", "残業", "シフト"]):
            return "打工劳动条件相关"
        if any(word in problem for word in ["诱导", "被骗", "高额", "説明と違う", "强制", "強制"]):
            return "消费者合同纠纷相关"
        return "一般消费生活问题"


class RelatedLawAgent:
    """
    相关制度判断 Agent
    作用：根据问题类型匹配可能相关的日本制度。
    """

    def analyze(self, category: str) -> str:
        if category == "购物、退货或取消相关":
            return "可能涉及店铺退货规则、通信販売规则、消费者保护制度"
        if category == "クーリング・オフ相关":
            return "可能涉及クーリング・オフ制度"
        if category == "租房或合同相关":
            return "可能涉及賃貸借契約、消費者契約法、民法"
        if category == "打工劳动条件相关":
            return "可能涉及労働基準法、労働契約法"
        if category == "消费者合同纠纷相关":
            return "可能涉及消費者契約法"
        return "可能涉及一般民事规则或消费者咨询制度"


class RiskAgent:
    """
    风险判断 Agent
    作用：粗略判断问题紧急程度。
    """

    def analyze(self, problem: str) -> str:
        high_words = ["今日まで", "马上", "立刻", "強制", "威胁", "脅し", "高额", "払え", "退去しろ"]
        middle_words = ["契約", "取消", "キャンセル", "工资", "給料", "家賃", "返品"]

        if any(word in problem for word in high_words):
            return "较高：建议尽快向学校、消费者中心或劳动咨询窗口确认"
        if any(word in problem for word in middle_words):
            return "中等：建议保存证据，并确认规则后再回复"
        return "较低：可以先整理信息，再咨询相关窗口"


class ExplanationAgent:
    """
    简单说明 Agent
    作用：用留学生也容易理解的语言解释。
    """

    def explain(self, category: str, related_law: str) -> str:
        if category == "购物、退货或取消相关":
            return (
                "如果是在普通店铺购买商品，日本法律上不一定无条件允许退货，很多时候要看店铺规则。"
                "如果是网购，也要先看网站写的返品・キャンセル规则。"
            )
        if category == "クーリング・オフ相关":
            return (
                "クーリング・オフ通常适用于访问销售、电话劝诱销售等特定交易。"
                "并不是所有购物都能使用クーリング・オフ，例如普通网购一般不一定适用。"
            )
        if category == "租房或合同相关":
            return (
                "租房问题要先确认契约书内容，但契约内容也不能违反法律或过度损害消费者利益。"
                "如果被突然要求退去、支付不明费用，建议先不要马上同意。"
            )
        if category == "打工劳动条件相关":
            return (
                "打工也受到劳动相关法律保护。工资、工作时间、加班、休息时间等不能只按店长随便决定。"
                "如果工资未支付或排班明显不合理，需要保存证据。"
            )
        if category == "消费者合同纠纷相关":
            return (
                "如果签约时有重要信息没有说明，或者被误导、被强迫签约，可能和消费者契约法有关。"
                "这种情况需要看具体证据和合同内容。"
            )
        return (
            "这个问题可能需要结合具体合同、聊天记录、收据或规则来判断。"
            "建议先整理证据，再向可靠窗口咨询。"
        )


class ActionAgent:
    """
    行动建议 Agent
    作用：给出下一步建议。
    """

    def suggest(self, category: str) -> str:
        common = (
            "1. 保存聊天记录、合同、收据、网页截图等证据。\n"
            "2. 不要急着口头答应或马上付款。\n"
            "3. 用简单日语向对方要求书面说明。\n"
        )

        if category == "打工劳动条件相关":
            return common + "4. 可以咨询学校学生支援课、労働基準監督署或外国人劳动咨询窗口。"
        if category == "租房或合同相关":
            return common + "4. 可以咨询学校、区役所的法律咨询、不动产相关咨询窗口。"
        return common + "4. 可以咨询消费者热线「188」或学校学生支援部门。"


class ConsumerLawAgentSystem:
    """
    消费法律小助手总控制系统：
    LawCategoryAgent → RelatedLawAgent → RiskAgent → ExplanationAgent → ActionAgent

    注意：本程序不是律师，不提供最终法律判断，只提供学习和整理思路用的初步参考。
    """

    def __init__(self):
        self.category_agent = LawCategoryAgent()
        self.related_law_agent = RelatedLawAgent()
        self.risk_agent = RiskAgent()
        self.explanation_agent = ExplanationAgent()
        self.action_agent = ActionAgent()

    def run(self, problem: str) -> dict:
        category = self.category_agent.analyze(problem)
        related_law = self.related_law_agent.analyze(category)
        risk_level = self.risk_agent.analyze(problem)
        explanation = self.explanation_agent.explain(category, related_law)
        action = self.action_agent.suggest(category)

        return {
            "category": category,
            "related_law": related_law,
            "risk_level": risk_level,
            "explanation": explanation,
            "action": action,
            "disclaimer": "本结果只是学习和生活参考，不是正式法律意见。重要问题请咨询学校、消费者中心、劳动咨询窗口或专业人士。"
        }
