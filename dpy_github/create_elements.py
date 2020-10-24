from abc import ABC, abstractmethod
from typing import List

from github import InputGitTreeElement
import discord

from . import format_model

class GitTreeElementCreator(ABC):
    """
    Discordモデルを受け取りInputGitTreeElementを作成して返す動作の抽象基底クラス。
    """

    @abstractmethod
    def create_channel_element(self, channel: discord.abc.GuildChannel) -> InputGitTreeElement:
        """
        サーバーのチャンネルを受け取りサーバー設定に依存する情報を抽出しInputGitTreeElementを作成します。
        """
        pass

    @abstractmethod
    def create_role_element(self, role: discord.Role) -> InputGitTreeElement:
        """
        サーバーのロールを受け取りサーバー設定に依存する情報を抽出しInputGitTreeElementを作成します。
        """
        pass

    @abstractmethod
    def create_member_element(self, member: discord.Member) -> InputGitTreeElement:
        """
        サーバーのメンバーを受け取りサーバー設定に依存する情報を抽出しInputGitTreeElementを作成します。
        """
        pass
    
    @abstractmethod
    def create_guild_element(self, guild: discord.Guild) -> InputGitTreeElement:
        """
        サーバーのメンバーを受け取りサーバー設定に依存する情報を抽出しInpuGitTreeElementを作成します。
        """
        pass

class DefaultTreeCreator(GitTreeElementCreator):
    """
    Discordモデルを受け取りInputGitTreeElementを作成して返す動作のデフォルト実装を定義します。
    """

    def __init__(self,**kwargs):
        user_formatter = kwargs.get("formatter")
        if user_formatter is not None and not isinstance(user_formatter, format_model.BaseFormatter):
            raise NotImplementedError(
                "formatter は format_model.BaseFormatter を実装している必要があります。"
                )
        if user_formatter is None:
            self.formatter = format_model.DefaultFormatter()
        else:
            self.formatter = user_formatter

    def create_channel_element(self, channel: discord.abc.GuildChannel) -> InputGitTreeElement:
        if channel.category_id is not None:
            file_path = f"channels/{channel.category_id}/{channel.id}.json"
        else:
            file_path = f"channels/{channel.id}.json"
        element = InputGitTreeElement(
            file_path,
            "100644",
            "blob",
            content=self.formatter.format_channel(channel)
        )
        return element

    def create_member_element(self, member: discord.Member) -> InputGitTreeElement:
        file_path = f"members/{member.id}.json"
        element = InputGitTreeElement(
            file_path,
            "100644",
            "blob",
            content=self.formatter.format_member(member)
        )
        return element

    def create_role_element(self, role: discord.Role) -> InputGitTreeElement:
        file_path = f"roles/{role.id}.json"
        element = InputGitTreeElement(
            file_path,
            "100644",
            "blob",
            content=self.formatter.format_role(role)
        )
        return element

    def create_guild_element(self, guild: discord.Guild) -> InputGitTreeElement:
        file_path = "guild_config.json"
        element = InputGitTreeElement(
            file_path,
            "100644",
            "blob",
            content=self.formatter.format_guild(guild)
        )
        return element

    def create_index_element(self, index_content) -> InputGitTreeElement:
        file_path = "index.md"
        element = InputGitTreeElement(
            file_path,
            "100644",
            "blob",
            content=index_content
        )
        return element
