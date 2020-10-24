from discord import VoiceRegion, VerificationLevel, ContentFilter, NotificationLevel

class PermissionTargets:
    Role = "ロール"
    Member = "メンバー"

class Channel:
    Name = "名前"
    ID = "ID"
    Position = "順番"
    Type = "タイプ"
    Overwrites = "権限上書き設定"
    Topic = "トピック"
    SlowModeDelay = "低速モード"
    Nsfw = "NSFWチャンネル設定"
    News = "ニュースチャンネル設定"
    BitRate = "ビットレート"
    UserLimit = "人数制限"

class Role:
    Name = "名前"
    Hoist = "オンラインメンバーとは別にロールメンバーを表示"
    Position = "順番"
    Mentionable = "このロールに対して@mentionを許可"
    Permission = "権限設定"
    Color = "色（RGB値）"

class Member:
    Nick = "ニックネーム"
    Roles = "ロールのIDリスト"

class Guild:
    Name = "名前"
    Region = "サーバー地域"
    AfkTimeout = "非アクティブタイムアウト時間"
    AfkChannelID = "休止チャンネルのID"
    IconURL = "アイコンのURL"
    OwnerID = "所有者のID"
    BannerURL = "バナー画像のURL"
    Description = "説明"
    MfaLevel = "2要素認証"
    VerificationLevel = "認証レベル"
    ExplicitContentFilter = "不適切なメディアコンテンツフィルター"
    DefaultNotifications = "標準の通知設定"
    SplashURL = "招待スプラッシュ画像のURL"
    PermiumTier = "サーバーブーストのレベル"
    PremiumSubscriptionCount = "サーバーのブースト数"

class GeneralConverter:
    @staticmethod
    def permission_name(perm_name: str) -> str:
        perm_name_meaning_dict = {
            "create_instant_invite": "招待の作成",
            "kick_members": "メンバーをキック",
            "ban_members": "メンバーをBAN",
            "administrator": "管理者",
            "manage_channels": "チャンネルの管理",
            "manage_guild": "サーバー管理",
            "add_reactions": "リアクションの追加",
            "view_audit_log": "監査ログを表示",
            "priority_speaker": "優先スピーカー",
            "stream": "動画（通話内）",
            "read_messages": "メッセージを読む",
            "view_channel": "メッセージを読む",
            "send_messages": "メッセージを送信",
            "send_tts_messages": "TTSメッセージを送信",
            "manage_messages": "メッセージの管理",
            "embed_links": "埋め込みリンク",
            "attach_files": "ファイルを送信",
            "read_message_history": "メッセージ履歴を読む",
            "mention_everyone": "@everyone、@here、全てのロールにメンション",
            "external_emojis": "外部の絵文字の使用",
            "use_external_emojis": "外部の絵文字の使用",
            "view_guild_insights": "サーバーインサイトの閲覧",
            "connect": "接続",
            "speak": "発言（通話内）",
            "mute_members": "メンバーをミュート",
            "deafen_members": "メンバーのスピーカーをミュート",
            "move_members": "メンバーを移動",
            "use_voice_activation": "音声検出を使用",
            "change_nickname": "ニックネームの変更",
            "manage_nicknames": "ニックネームの管理",
            "manage_roles": "ロールの管理",
            "manage_permissions": "ロールの管理",
            "manage_webhooks": "ウェブフックの管理",
            "manage_emojis": "絵文字の管理"
        }

        return perm_name_meaning_dict.get(perm_name,perm_name)

    @staticmethod
    def region_name(region: VoiceRegion) -> str:
        region_name_meaning_dict = {
            VoiceRegion.amsterdam: "アムステルダム",
            VoiceRegion.brazil: "ブラジル",
            VoiceRegion.dubai: "ドバイ",
            VoiceRegion.eu_central: "中央ヨーロッパ",
            VoiceRegion.eu_west: "東ヨーロッパ",
            VoiceRegion.europe: "ヨーロッパ",
            VoiceRegion.frankfurt: "フランクフルト",
            VoiceRegion.hongkong: "香港",
            VoiceRegion.india: "インド",
            VoiceRegion.japan: "日本",
            VoiceRegion.london: "ロンドン",
            VoiceRegion.russia: "ロシア",
            VoiceRegion.singapore: "シンガポール",
            VoiceRegion.southafrica: "南アフリカ",
            VoiceRegion.sydney: "シドニー",
            VoiceRegion.us_central: "中央アメリカ",
            VoiceRegion.us_west: "アメリカ西部",
            VoiceRegion.us_east: "アメリカ東部",
            VoiceRegion.us_south: "アメリカ南部",
            VoiceRegion.vip_us_east: "VIP用アメリカ東部サーバー",
            VoiceRegion.vip_us_west: "VIP用アメリカ西部サーバー",
            VoiceRegion.amsterdam: "VIP用アムステルダムサーバー",
        }
        return region_name_meaning_dict.get(region, region)

    @staticmethod
    def verification_level(level: VerificationLevel) -> str:
        verification_level_meaning_dict = {
            VerificationLevel.low: "低：メール認証がされているアカウントのみ",
            VerificationLevel.medium: "中：Discordに登録してから5分以上経過したアカウントのみ",
            VerificationLevel.high: "高：このサーバーのメンバーとなってから10分以上経過したメンバーのみ",
            VerificationLevel.very_high: "最高：電話認証がされているアカウントのみ",
            VerificationLevel.table_flip: "高：このサーバーのメンバーとなってから10分以上経過したメンバーのみ",
            VerificationLevel.extreme: "最高：電話認証がされているアカウントのみ",
            VerificationLevel.double_table_flip: "最高：電話認証がされているアカウントのみ"
        }
        return verification_level_meaning_dict.get(level,level)

    @staticmethod
    def explicit_content_filter(filter_: ContentFilter) -> str:
        content_fileter_meaning_dict = {
            ContentFilter.disabled: "いかなるメディアコンテンツもスキャンしない",
            ContentFilter.no_role: "ロールのないメンバーのメディアコンテンツをスキャン",
            ContentFilter.all_members: "全てのメンバーのメディアコンテンツをスキャン"
        }
        return content_fileter_meaning_dict.get(filter_, filter_)

    @staticmethod
    def notification_level(level: NotificationLevel) -> str:
        notification_levl_meaning_dict = {
            NotificationLevel.all_messages: "すべてのメッセージ",
            NotificationLevel.only_mentions: "@mentionsのみ"
        }
        return notification_levl_meaning_dict.get(level, level)

class BooleanConverter:
    @staticmethod
    def yes_no(value: bool) -> str:
        return ["いいえ", "はい"][value]

    @staticmethod
    def has_permission(value: bool) -> str:
        return ["不可","可"][value]

    @staticmethod
    def do(value: bool) -> str:
        return ["しない","する"][value]

    @staticmethod
    def valid(value: bool) -> str:
        return ["無効","有効"][value]