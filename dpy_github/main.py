from typing import List
import sys
from string import Template

import github
import discord

from . import util
from . import create_elements

class Reporter:
    """Discordサーバーの情報をGitHubに記録する起点。
    """    
    
    def __init__(self, guild: discord.Guild, github_token: str, repository_name:str, 
        branch_name:str="main", element_creator:create_elements.GitTreeElementCreator=None, allow_new_repository=False):
        """[summary]
        Args:
            guild (discord.Guild): 記録を行うサーバー。
            github_token (str): GitHubアカウントのアクセストークン。
            repository_name (str): リポジトリ名。
            branch_name (str, optional): 記録を行うブランチ名. Defaults to "main".
            element_creator (create_elements.GitTreeElementCreator, optional): GitTreeの生成を行うオブジェクト。 Defaults to None.
            allow_new_repository (str, optional): もし repository_name に該当するリポジトリが見つからなかったとき、Trueなら新規作成します。

        Raises:
            NotImplementedError: element_creator は create_elements.GitTreeElementCreator を実装している必要があります。
        """        
        self.branch_name = branch_name
        if not isinstance(element_creator, create_elements.GitTreeElementCreator):
            if element_creator is None:
                self.element_creator = create_elements.DefaultTreeCreator()
            else:
                raise NotImplementedError(
                    "element_creator は create_elements.GitTreeElementCreatorを実装している必要があります。"
                    )
        self.ref_name = "heads/" + self.branch_name

        self.guild = guild
        self.github_client = github.Github(github_token)
        try:
            self.repository: github.Repository = self.github_client.get_user().get_repo(repository_name)
        except github.UnknownObjectException:
            if not allow_new_repository:
                raise ValueError(f"{repository_name} という名前のリポジトリは見つかりませんでした。")
            else:
                self.repository: github.Repository = self.github_client.get_user().create_repo(repository_name,auto_init=True)


    def create_index_content(self, by_category, members, roles, template_path="template.md"):
        channel_text_list = []
        channel_url_base = f"{self.repository.html_url}/blob/{self.branch_name}/channels"
        for category, channels in by_category:
            if category is not None:
                channel_url = f"{channel_url_base}/{category.id}.json"
                channel_text_list.append(f"- [{category.name}]({channel_url}) *[{category.type[0]}]*")
            
            for channel in channels:
                channel_url = f"{channel_url_base}/{category.id}/{channel.id}.json"
                channel_text_list.append(f"\t- [{channel.name}]({channel_url}) *[{channel.type[0]}]*")

        member_text_list = []
        for member in members:
            member_url = f"{self.repository.html_url}/blob/{self.branch_name}/members/{member.id}.json"
            member_text_list.append(f"- [{member.name}]({member_url})")

        role_text_list = []
        for role in roles:
            role_url = f"{self.repository.html_url}/blob/{self.branch_name}/roles/{role.id}.json"
            role_text_list.append(f"- [{role.name}]({role_url})")
            
        with open(template_path, "r",encoding="utf-8") as f:
            lines = f.readlines()
        template = Template("\n".join(lines))

        return template.substitute(
            GUILD_NAME=self.guild.name, CHANNEL_LIST="\n".join(channel_text_list), 
            ROLE_LIST="\n".join(role_text_list), MEMBER_LIST="\n".join(member_text_list)
        )

    def create_git_tree(self) -> github.GitTree:
        """element_creatorを利用してgithub.GitTreeを作成し返します。

        Returns:
            github.GitTree: 作成されたGitTree。
        """        
        channel_elements = []
        sorted_by_category = util.sort_category_position(self.guild.by_category())
        for category, channels in sorted_by_category:
            if category is not None:
                channel_elements.append(self.element_creator.create_channel_element(category))

            for channel in channels:
                channel_elements.append(self.element_creator.create_channel_element(channel))

        member_elements = []
        for member in self.guild.members:
            member_elements.append(self.element_creator.create_member_element(member))

        role_elements = []
        for role in self.guild.roles:
            role_elements.append(self.element_creator.create_role_element(role))
        
        guild_element = self.element_creator.create_guild_element(self.guild)

        index_element = self.element_creator.create_index_element(
            self.create_index_content(sorted_by_category, self.guild.members, self.guild.roles)
            )

        tree = self.repository.create_git_tree(channel_elements + role_elements + member_elements + [index_element, guild_element])
        return tree

    def push(self,commit_title="commit") -> str:
        """GitHubに実際にサーバー情報を保存します。

        Args:
            commit_title (str, optional): コミットのタイトルです。 Defaults to "commit".

        Returns:
            str: 編集を行ったリポジトリのGitHub上のURL。
        """        
        tree = self.create_git_tree()

        repo = self.repository
        ref = repo.get_git_ref(self.ref_name)
        
        parents = [repo.get_git_commit(c.sha) for c in repo.get_commits()]
        commit = repo.create_git_commit(commit_title,tree,parents)
        ref.edit(commit.sha,force=True)
        return repo.html_url
