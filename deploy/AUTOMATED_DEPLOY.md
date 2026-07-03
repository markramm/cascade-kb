# Automated deploys for capturecascade.org

> **STATUS (2026-07-03): LIVE.** Every push to `main` that touches
> `cascade-timeline/`, `hugo-timeline/`, `deploy/`, or the workflow auto-deploys
> to the VPS via GitHub Actions (`.github/workflows/deploy.yml`) using a
> dedicated `deploy`-user SSH key. Secrets are set; the first green run was
> 2026-07-03. Deploy takes ~12-17 min (OG-card generation dominates).
>
> **Safety rails in `deploy/deploy.sh`:**
> - Zero-downtime: the front-end Caddy is only reloaded after health + content
>   checks pass; a failed build never takes the live site down (proven).
> - Build-cache reclaim every run (safe on the shared host; freed 76 GB once).
> - Content verification: fetches real page bodies and asserts keywords, not
>   just HTTP status. Uses `grep -c` (not `grep -q`) to avoid a pipefail
>   false-positive.
> - Rollback: restarts the last-known-good IMAGE (no rebuild) if health or
>   content checks fail.
> - The CI workflow pulls BEFORE invoking deploy.sh, so the running script is
>   always current (deploy.sh pulling itself ran the pre-pull version — fixed).
>
> **Known follow-up:** the ~12-min build is dominated by ~260 s regenerating
> all 400 OG-card PNGs every build (Docker discards them between builds). A
> Docker cache-mount on the OG-cards dir would cut deploys to ~4 min.

---

## One-time bootstrap

These steps run once, on the VPS as the admin/root user. The `deploy`
user already exists (created by `pyrite/deploy/demo/setup-server.sh`
and used by `cascade-kb/deploy/setup-server.sh`).

### 1. Generate an SSH keypair dedicated to this workflow

On your local machine (not the VPS):

```bash
ssh-keygen -t ed25519 -f ~/.ssh/cascade-deploy -C "github-actions-cascade-deploy" -N ""
```

You'll get two files:
- `~/.ssh/cascade-deploy`     — private key (goes to GitHub secrets)
- `~/.ssh/cascade-deploy.pub` — public key (goes to VPS)

### 2. Install the public key on the VPS for the `deploy` user

```bash
# As admin on VPS:
sudo mkdir -p /home/deploy/.ssh
sudo tee -a /home/deploy/.ssh/authorized_keys < ~/.ssh/cascade-deploy.pub > /dev/null
sudo chown -R deploy:deploy /home/deploy/.ssh
sudo chmod 700 /home/deploy/.ssh
sudo chmod 600 /home/deploy/.ssh/authorized_keys
```

Then verify from your local machine:

```bash
ssh -i ~/.ssh/cascade-deploy deploy@<vps-host> "whoami && docker info | head -3"
# Expect:
#   deploy
#   Client: Docker Engine ...
```

If that works, the deploy user has SSH access and can talk to Docker.

### 3. Add GitHub secrets

In the cascade-kb repo settings → Secrets and variables → Actions → New
repository secret. Add three (port is optional):

| Name                       | Value                                       |
|----------------------------|---------------------------------------------|
| `CASCADE_DEPLOY_HOST`      | VPS hostname or IP (e.g. `demo.pyrite.wiki`) |
| `CASCADE_DEPLOY_USER`      | `deploy`                                    |
| `CASCADE_DEPLOY_SSH_KEY`   | **Contents** of `~/.ssh/cascade-deploy` (the private key, including the `-----BEGIN/END-----` lines) |
| `CASCADE_DEPLOY_PORT`      | Only if SSH is on a non-22 port            |

### 4. Test the workflow manually

In the GitHub repo: Actions → "Deploy capturecascade.org" → Run workflow
→ branch: main → Run workflow.

Watch the log. The deploy script will:

1. `git pull --ff-only`
2. Print `docker system df`, skip the prune prompt
3. Build the cascade image (~few minutes for the Hugo + sitemap build)
4. Restart the container
5. Wait for healthcheck
6. Verify the front-end Caddyfile points at `cascade:8088` (already
   true; no patch happens)
7. Reload the front-end Caddy
8. Run three verification curls (root, public, redirect)

A successful run ends with `──── Done ────` and the three verification
HTTP/2 200 / 301 lines.

### 5. Flip the workflow to auto-trigger on push

Once the manual run works, edit `.github/workflows/deploy.yml`:

```yaml
on:
  push:
    branches: [main]
  workflow_dispatch:
```

Commit + push. That push itself triggers the first auto-deploy.

## Failure behavior

- **Build fails**: Docker compose doesn't replace the running container.
  The site stays up on the previous image. GitHub emails you the failure.
- **SSH unreachable**: workflow fails fast (~30s). GitHub emails you.
- **Healthcheck never passes**: deploy.sh exits non-zero after 60s of
  retries. GitHub emails you. Investigate by SSHing in and running
  `docker compose -f ~/cascade-kb/deploy/docker-compose.yml logs cascade`.

No Slack/Discord notification is wired up — GitHub's built-in failure
emails are the only channel. Add one to `.github/workflows/deploy.yml`
if email is missed in practice.

## Manual deploys still work

Nothing about the automated setup blocks the original manual flow.
SSH in, `cd ~/cascade-kb`, `bash deploy/deploy.sh` (without
`--no-interactive`) still works exactly as before.
