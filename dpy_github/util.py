from typing import List, Tuple, Optional
import json
from string import Template

import github
import discord

def sort_category_position(by_category:List[Tuple[Optional[discord.CategoryChannel], List[discord.abc.GuildChannel]]]):
    """
    by_category() の戻り値である CategoryChannel 、discord.abc.GuildChannelのリストで構成されるタプルのリストを順番でソートします。
    """

    # 入れ子になっているチャンネルを先にソート
    categories_sorted_children = []
    for category, channels in by_category:
        if category is None:
            categories_sorted_children.append((None,[channels]))
        else:
            categories_sorted_children.append((category, sorted(channels, key=lambda channel: channel.position)))

    def sort_channel_key(category_and_channels):
        category, channels = category_and_channels
        if category is None:
            print(channels)
            return channels[0].position
        else:
            return category.position

    # トップレベルのチャンネルをソート
    return sorted(categories_sorted_children, key=sort_channel_key)
