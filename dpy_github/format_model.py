from abc import ABC, abstractmethod
from typing import Mapping, Union
import json

import discord

from . import i18n

class BaseFormatter(ABC):
    """Discordモデルを文字列に整形する動作の抽象基底クラス。
    """
    @abstractmethod
    def format_channel(self, channel: discord.abc.GuildChannel) -> str:
        pass

    @abstractmethod
    def format_member(self, member: discord.Member) -> str:
        pass

    @abstractmethod
    def format_role(self, role: discord.Role) -> str:
        pass

    @abstractmethod
    def format_guild(self, guild: discord.Guild) -> str:
        pass

class DefaultFormatter(BaseFormatter):
    def dumps(self, json_data: dict) -> str:
        return json.dumps(json_data, sort_keys=True, indent=4, ensure_ascii=False)

    def format_permission_dict(self, permission: Mapping[
        Union[discord.Role,discord.Member],Union[discord.Permissions,discord.PermissionOverwrite
        ]]) -> dict:
        permission_data = {
            i18n.PermissionTargets.Role: {},
            i18n.PermissionTargets.Member: {}
        }

        for target in permission:
            converted_permission = {
                i18n.GeneralConverter.permission_name(perm):
                i18n.BooleanConverter.has_permission(value)
                for perm, value in permission[target] if value is not None
            }
            if isinstance(target,discord.Role): 
                permission_data[i18n.PermissionTargets.Role][target.id] = converted_permission
            elif isinstance(target,discord.Member):
                permission_data[i18n.PermissionTargets.Member][target.id] = converted_permission

        return permission_data

    def format_permission_of_role_dict(self, permission: discord.Permissions) -> dict:
        permission_data = {}
        for perm, value in permission:
            permission_data[i18n.GeneralConverter.permission_name(perm)] = i18n.BooleanConverter.has_permission(value)
        return permission_data


    def format_channel(self, channel: discord.abc.GuildChannel) -> str:
        channel_data = {
            i18n.Channel.Name: channel.name,
            i18n.Channel.ID: channel.id,
            i18n.Channel.Position: channel.position,
            i18n.Channel.Type: channel.type[0],
            i18n.Channel.Overwrites: self.format_permission_dict(channel.overwrites)
        }

        if isinstance(channel, discord.TextChannel):
            channel_data[i18n.Channel.Topic] = channel.topic
            channel_data[i18n.Channel.SlowModeDelay] = channel.slowmode_delay
            channel_data[i18n.Channel.Nsfw] = i18n.BooleanConverter.yes_no(channel.is_nsfw())
            channel_data[i18n.Channel.News] = i18n.BooleanConverter.yes_no(channel.is_news())

        if isinstance(channel, discord.VoiceChannel):
            channel_data[i18n.Channel.BitRate] = channel.bitrate
            channel_data[i18n.Channel.UserLimit] = channel.user_limit

        if isinstance(channel, discord.CategoryChannel):
            channel_data[i18n.Channel.Nsfw] = i18n.BooleanConverter.yes_no(channel.is_nsfw())

        return self.dumps(channel_data)

    def format_role(self, role: discord.Role) -> str:
        role_data = {
            i18n.Role.Name: role.name,
            i18n.Role.Hoist: i18n.BooleanConverter.yes_no(role.hoist),
            i18n.Role.Position: role.position,
            i18n.Role.Mentionable: i18n.BooleanConverter.has_permission(role.mentionable),
            i18n.Role.Permission: self.format_permission_of_role_dict(role.permissions),
            i18n.Role.Color: str(role.color.to_rgb())
        }
        return self.dumps(role_data)

    def format_member(self, member: discord.Member) -> str:
        member_data = {
            i18n.Member.Nick: member.nick,
            i18n.Member.Roles: [str(role.id) for role in member.roles][1:]
        }
        return self.dumps(member_data)

    def format_guild(self, guild: discord.Guild) -> str:
        guild_data = {
            i18n.Guild.Region: i18n.GeneralConverter.region_name(guild.region),
            i18n.Guild.AfkTimeout: guild.afk_timeout,
            i18n.Guild.AfkChannelID: guild.afk_channel.id if guild.afk_channel is not None else "",
            i18n.Guild.IconURL: str(guild.icon_url),
            i18n.Guild.OwnerID: guild.owner_id,
            i18n.Guild.BannerURL: str(guild.banner_url),
            i18n.Guild.Description: guild.description,
            i18n.Guild.MfaLevel: i18n.BooleanConverter.valid(guild.mfa_level),
            i18n.Guild.VerificationLevel: i18n.GeneralConverter.verification_level(guild.verification_level),
            i18n.Guild.ExplicitContentFilter: i18n.GeneralConverter.explicit_content_filter(guild.explicit_content_filter),
            i18n.Guild.DefaultNotifications: i18n.GeneralConverter.notification_level(guild.default_notifications),
            i18n.Guild.SplashURL: str(guild.splash_url),
            i18n.Guild.PermiumTier: guild.premium_tier,
            i18n.Guild.PremiumSubscriptionCount: guild.premium_subscription_count
        }
        return self.dumps(guild_data)
