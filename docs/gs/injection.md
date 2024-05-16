# Injection

Below is an explanation of how ongaku supports injection.

!!! warning "support"
    Please note, that only the command handlers [tanjun]() and [arc]() are currently supported with ongaku's dependency injection.

Ongaku relies on the framework [alluka]() for its dependency injection support.


=== "Arc"

    First of all, for the injection to work, you need to use `.from_arc()` client creation

    ```py linenums="1"
    bot = hikari.GatewayBot(...)
    client = arc.GatewayClient(bot)
    ongaku_client = ongaku.Client.from_arc(client)
    ```

    lets explain what each line does.

    ```py linenums="1"
    bot = hikari.GatewayBot(...)
    ```
    This line simply sets up your GatewayBot.

    ```py linenums="2"
    client = arc.GatewayClient(bot)
    ```
    This sets up the arc client (your command handler.)

    ```py linenums="3"
    ongaku_client = ongaku.Client.from_arc(client)
    ```
    Finally, this sets up ongaku's client.

    Now, there is a few ways to use ongaku's client.

    The first method is good for creating players, and fetching new songs.

    ```py linenums="1"
    @arc.slash_command("example", "This is an example command")
    async def example_command(
        ctx: arc.GatewayContext,
        ongaku_client: ongaku.Client = arc.Inject()
    ) -> None:
        ...
    ```

    Now, if you just wish to get a player directly without having to fetch it, the best method would be the following:

    ```py linenums="1"
    @arc.slash_command("example", "This is an example command")
    async def example_command(
        ctx: arc.GatewayContext,
        ongaku_client: ongaku.Player = arc.Inject()
    ) -> None:
        ...
    ```

    You can still get the client from a player, simply by using `player.client`

    !!! warning
        When using this method, two things will result in an exception.

        1. If the current command is not ran in a guild, it will error out.
        2. If the current guild does not have a valid player.


=== "Tanjun"

    First of all, for the injection to work, you need to use `.from_tanjun()` client creation

    ```py linenums="1"
    bot = hikari.GatewayBot(...)
    client = tanjun.Client.from_gateway_bot(bot)
    ongaku_client = ongaku.Client.from_tanjun(client)
    ```

    lets explain what each line does.

    ```py linenums="1"
    bot = hikari.GatewayBot(...)
    ```
    This line simply sets up your GatewayBot.

    ```py linenums="2"
    client = tanjun.Client.from_gateway_bot(bot)
    ```
    This sets up the tanjun client (your command handler.)

    ```py linenums="3"
    ongaku_client = ongaku.Client.from_tanjun(client)
    ```
    Finally, this sets up ongaku's client.

    ```py linenums="1"
    @tanjun.as_slash_command("name", "description")
    async def some_command(
        ctx: tanjun.abc.SlashContext, 
        ongaku_client: ongaku.Client = alluka.inject()
    ) -> None:
        ...
    ```

    !!! warning
        Tanjun does not currently support player injection.