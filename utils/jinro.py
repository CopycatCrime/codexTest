from typing import List, Dict, Optional

class Member:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.alive = True      # 生存状況
        self.can_act = False   # 夜のターンに行動可能かどうか

    def start_night(self) -> None:
        """夜フェーズ開始時に呼び出し、行動フラグを立てる"""
        self.can_act = True

    def end_night(self) -> None:
        """行動終了後に呼び出し、行動フラグをリセット"""
        self.can_act = False

    def act(self, target: Optional['Member'] = None) -> None:
        """夜ターンのアクション。サブクラスでオーバーライド"""
        raise NotImplementedError("Subclasses must implement this method")


class Villager(Member):
    def __init__(self,
                 name: str = "Villager",
                 description: str = "普通の村人。夜の特別な能力はない。"):
        super().__init__(name, description)

    def act(self, target: Optional[Member] = None) -> None:
        if not self.can_act:
            print(f"{self.name}：夜に行動できません。")
        else:
            print(f"{self.name}：この夜は特に行動しませんでした。")
        self.end_night()


class Seer(Member):
    def __init__(self,
                 name: str = "Seer",
                 description: str = "占い師。夜に1人の役職を知ることができる。"):
        super().__init__(name, description)

    def act(self, target: Optional[Member]) -> None:
        if not self.can_act:
            print(f"{self.name}：行動できません。")
            return
        if target:
            print(f"{self.name}：{target.name} の役職は {target.__class__.__name__} です。")
        else:
            print(f"{self.name}：対象が指定されていません。")
        self.end_night()


class Werewolf(Member):
    def __init__(self,
                 name: str = "Werewolf",
                 description: str = "人狼。夜に1人を襲撃できる。"):
        super().__init__(name, description)

    def act(self, target: Optional[Member]) -> None:
        if not self.can_act:
            print(f"{self.name}：行動できません。")
            return
        if target and target.alive:
            target.alive = False
            print(f"{self.name}：{target.name} を襲撃し、{target.name} は死亡しました。")
        elif target:
            print(f"{self.name}：{target.name} は既に死亡しています。")
        else:
            print(f"{self.name}：対象が指定されていません。")
        self.end_night()


class Madman(Member):
    def __init__(self,
                 name: str = "Madman",
                 description: str = "狂人。夜のターンに人狼と同じく襲撃可能だが、自分は人狼ではないと信じている。"):
        super().__init__(name, description)

    def act(self, target: Optional[Member]) -> None:
        if not self.can_act:
            print(f"{self.name}：行動できません。")
            return
        if target and target.alive:
            target.alive = False
            print(f"{self.name}：{target.name} を襲撃し、{target.name} は死亡しました。")
        elif target:
            print(f"{self.name}：{target.name} は既に死亡しています。")
        else:
            print(f"{self.name}：対象が指定されていません。")
        self.end_night()


# 役職名と説明の定義
roles: Dict[str, str] = {
    "Villager": "普通の村人。夜に能力なし。",
    "Seer": "占い師。夜に1人の役職を知ることができる。",
    "Werewolf": "人狼。夜に1人を襲撃できる。",
    "Madman": "狂人。夜のターンに人狼と同じく襲撃可能だが、自分は人狼ではないと信じている。"
}


class Jinro:
    def __init__(self, members: List[Member], max_turns: int):
        """
        人狼ゲーム本体クラス。
        members: メンバーインスタンスのリスト
        max_turns: ゲーム終了までの最大ターン数（外部からは参照不可）
        """
        self._members = members
        self._turn = 0
        self.__rope = max_turns  # プレイヤーからは取得できない縄数

    def get_turn(self) -> int:
        """現在のターンを返す"""
        return self._turn

    def start_night_phase(self) -> None:
        """夜フェーズ開始: 全員の行動フラグを有効化"""
        for m in self._members:
            if m.alive:
                m.start_night()

    def execute_night_actions(self, actions: Dict[Member, Optional[Member]]) -> None:
        """
        actions: 各行動役職から対象へのマッピング
        Night のアクションを順に実行する
        """
        for actor, target in actions.items():
            if actor.alive:
                actor.act(target)

    def end_night_phase(self) -> None:
        """夜フェーズ終了: ターン数と縄数を更新"""
        for m in self._members:
            m.end_night()
        self._turn += 1
        self.__rope -= 1

    def is_game_over(self) -> bool:
        """縄数が尽きたらゲーム終了"""
        return self.__rope <= 0

    def get_alive_members(self) -> List[Member]:
        """生存中メンバーのリストを返す"""
        return [m for m in self._members if m.alive]

    # 注意: 縄数 (__rope) は外部アクセスを意図的に提供しない
