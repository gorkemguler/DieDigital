# 2. Content cleanup

Delete your content before you close your accounts:

- Some platforms keep your content after you delete the account (Reddit, Discord, Stack Overflow, many forums and comment systems).
- If something goes wrong during the deletion waiting period, at least the content is already gone.
- If you're aiming for level 1 (invisible) and keeping your accounts, content cleanup is the main job.

## General method

1. **Hide first, then delete.** On day one, make the account private or archive your posts. That cuts off public visibility in minutes, and you can delete at your own pace afterwards.
2. **Start with the most dangerous items:** photos showing your face, posts with locations, anything mentioning your phone number, address, school or workplace, comments posted under your real name.
3. **Find the platform's activity page.** Most have bulk select and delete.
4. **Be careful with bulk-deletion apps.** Third-party apps that want your password or full account access are a new risk. Use the platform's own tools where possible, otherwise open-source tools you trust, and revoke their access when you're done.
5. **Check from the outside:** log out, open your profile in a private window and see what's still visible.

## Facebook

- **Hide quickly:** Settings > Privacy > "Who can see your future posts: Only me" and "Limit past posts".
- **Bulk delete:** Profile > ⋯ > Activity log > Your activity. In the Posts, Comments, Likes and reactions, and Posts you're tagged in categories, select in bulk > Move to trash / Remove.
- **Photos:** Profile and cover photo albums are separate, and old profile photos are usually public.
- **Tags:** Remove your tag from other people's posts. For the posts themselves, see chapter 6.
- **Groups and Pages:** Your group posts and comments are listed separately. Delete or hand over the Pages and groups you manage, then leave.
- **Messenger:** Deleting a conversation only deletes your copy.
- **Marketplace listings:** Old listings can still show your photos and location.

## Instagram and Threads

- **Hide:** Settings > Account privacy > Private account.
- **Bulk delete:** Profile > ☰ > Your activity > Photos and videos / Comments / Likes / Story replies > Select > Delete.
- **Archive:** The story archive and "Archived" posts must be deleted too; archived is not deleted.
- **Tags:** Profile > Tagged; remove your tag from each. Settings > Tags and mentions > Who can tag you: No one.
- **Contact syncing:** Accounts Center > Your information and permissions > Upload contacts: turn it off. Turning it off also deletes the contacts you uploaded.

## X (Twitter)

- **Hide:** Settings > Privacy and safety > Audience > Protect your posts. Your posts drop out of search and public view immediately.
- **Delete:** Bulk deletion through the free API isn't practical. Delete sensitive posts one by one; the rest go when the account is deleted (30 days after deactivation).
- **Likes, bookmarks, lists, Communities:** clean these up separately.
- Quote posts and screenshots belong to other people; you can't delete those.

## TikTok

Profile > videos: each video > ⋯ > Delete. Your comments and favourites list need cleaning up separately. Quick protection: Settings and privacy > Privacy > Private account.

## YouTube and Google

- **Your videos:** YouTube Studio > Content > select all > Delete forever. Setting them to "Private" first gives you quick protection.
- **Comments on other people's videos:** https://myactivity.google.com/page?page=youtube_comments. These can survive even if you delete your channel.
- **Playlists and subscriptions:** Make public playlists private or delete them; hide your subscriptions.
- **Google Maps:** Maps > Contributions > Reviews, Photos, Edits. Local Guide reviews show your name and profile photo, and a lot of people forget about them.
- **Blogger, Google Sites:** Delete your blogs and sites.
- **Google Drive:** Files shared as "Anyone with the link" can get indexed. Go through Shared items in Drive and turn sharing off.
- **Google Photos:** Shared albums and links.

## LinkedIn

- **Activity:** Profile > Activity > Posts / Comments / Reactions; delete each one.
- **Profile:** Remove your photo, work history, education, endorsements and recommendations. If you're keeping the account: Settings > Visibility > Public profile: off.
- **Contact uploads:** Settings > Data privacy > Sync contacts: turn it off and delete the uploaded contacts.

## Reddit

Your comments stay up after the account is deleted. The best approach is to overwrite each comment and text post with meaningless text and then delete it: the last version of deleted content can survive in some third-party archives, and overwriting at least makes that last version meaningless.

- **By hand:** Profile > Comments > each comment > ⋯ > Edit (replace the text with ".") > Save > Delete. Same for posts.
- Reddit listings show at most around 1,000 items. For older ones, request your data at https://www.reddit.com/settings/data-request; the archive contains links to all your comments.

> **With the tool:** `diedigital wipe reddit` does this automatically, including the `comments.csv` / `posts.csv` files from your data export.

## Discord

Your messages stay after the account is deleted (as "Deleted User").

- **By hand:** Delete your messages in the servers and DMs that matter (hover over the message > Delete).
- **In bulk:** Tools that delete messages automatically from your own account (self-bots) break Discord's rules. The proper route: request your data package (Settings > Data & Privacy), pull out the IDs of the channels you posted in, and use Discord's privacy request form to ask for your messages in those channels to be deleted.
- Delete or transfer the servers you own.

## Messaging apps

- **Telegram:** In private chats you can delete the history for both sides at any time ("Also delete for ..."). In groups you can delete your own messages; do it before you leave the group. Delete or transfer channels and groups you own.
- **WhatsApp:** "Delete for everyone" only works for a short time after sending. Older messages stay on the other person's phone; for important ones your only option is to ask them to delete them ([Appendix B](appendix-b-letter-templates.md) has a message you can use). Turn off status and profile photo visibility.
- **Signal:** Chats live on devices; disappearing messages delete them on the other side too.

## Developer platforms

- **GitHub:** Settings > Repositories: delete each repository (Settings > Danger Zone > Delete). Delete your gists. Clear the name, bio, location, company and website fields on your profile. Commits, issues and comments you made in other people's repositories stay; the email address in your commits stays unless the repository owner rewrites history. From now on, use GitHub's `noreply` address.
- **GitLab, Bitbucket:** Projects and snippets, the same way.
- **Stack Overflow:** Content is licensed CC BY-SA; when you delete your profile it's anonymised but stays. You can delete your own questions and answers that haven't been accepted.
- **npm, PyPI, Docker Hub:** Packages you published may contain your name and email. Deleting a package can break other people's projects; consider transferring ownership instead.

> **With the tool:** `diedigital wipe github` deletes repositories and gists and clears your profile.

## Other social and content sites

- **Mastodon:** Preferences > Automated post deletion lets the server do it, or delete posts one by one. (With the tool: `diedigital wipe mastodon`)
- **Pinterest:** Delete boards or make them secret.
- **Tumblr, Medium, WordPress.com, Blogger:** Delete posts and comments, then the blog.
- **Quora:** Answers, questions, comments.
- **Spotify:** Make public playlists private; change your display name (it may be your real name).
- **Strava and fitness apps:** Delete activities or set them to "Only you". Public running maps reveal your home address ([chapter 7](07-real-world-traces.md)).
- **Foursquare / Swarm:** Delete your check-in history; it's a map of where you've been for years.
- **Letterboxd, Goodreads, Last.fm, Duolingo:** Profiles are usually public.
- **Photo sites:** Flickr, 500px, Unsplash, VSCO.

## Comments and reviews

- **Google Maps reviews** (above), **TripAdvisor, Booking.com and Airbnb reviews**, app store reviews.
- **Complaint and review sites:** Your complaints and reviews often appear under your full name. Remove them in your account settings or through support.
- **News site comments and Disqus:** In Disqus, go to your profile > comments; on news sites with their own login, sign in and delete your comments.
- **Forums:** Delete what you wrote first, then close the account. For content you can't delete, write to the admins ([Appendix B](appendix-b-letter-templates.md)); requests that cite data protection law get taken more seriously.
- **Wikipedia:** Remove your user page and anything you wrote about yourself. If there's an article about you, see chapter 6.

## Your own website or blog

To make search engines drop a page quickly:

1. Before removing the page, add `<meta name="robots" content="noindex">` and wait a few days.
2. Then delete the page and have the server return **410 Gone** (it drops out faster than a 404).
3. Verify the site in Google Search Console and use the "Removals" tool.
4. Decide what to do with the domain in [chapter 9](09-final-steps.md): letting a domain expire carries a security risk.

## End-of-chapter checklist

- [ ] The accounts I'm keeping are private
- [ ] Photos, posts with locations and comments under my real name are deleted
- [ ] On platforms that keep content after account deletion (Reddit, Discord, forums, Stack Overflow), the content is cleaned up
- [ ] Reviews and comments (Maps, review sites, app stores) are deleted
- [ ] Contact syncing is off and uploaded contacts are deleted
- [ ] I've checked from a private window and nothing is visible
