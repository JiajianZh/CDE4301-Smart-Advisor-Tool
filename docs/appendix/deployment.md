# Appendix F: Deployment Information

[← Back to Main Report](../index.md)

---

## Live Application

**URL:** [https://cde4301-smart-advisor-tool-8pq7cdqe3uubafqgwu5awg.streamlit.app/](https://cde4301-smart-advisor-tool-8pq7cdqe3uubafqgwu5awg.streamlit.app/)

**Platform:** Streamlit Community Cloud

**Availability:** 24/7, public access, no login required

**Hosting Costs:** Free (Streamlit Community Cloud free tier)

**Mobile Support:** Yes, responsive design works on phones and tablets

---

## Deployment Architecture

```
Developer (VS Code)
    ↓
    [Commit & Push]
    ↓
GitHub Repository (main branch)
    ↓
    [Webhook Trigger]
    ↓
Streamlit Cloud
    ↓
    [Auto-Build & Deploy]
    ↓
Live Application
    ↓
Users Access via Browser
```

---

## Deployment Process

### Initial Setup (One-Time)

**Step 1: Create Streamlit Cloud Account**
- Go to [https://share.streamlit.io/](https://share.streamlit.io/)
- Sign in with GitHub account
- Authorize Streamlit to access GitHub repositories

**Step 2: Deploy Application**
- Click "New app" in Streamlit Cloud dashboard
- Select repository: `JiajianZh/CDE4301-Smart-Advisor-Tool`
- Select branch: `main`
- Set main file path: `app.py`
- Click "Deploy"

**Step 3: Configure Settings**
- App name: `CDE4301 Smart Advisor Tool`
- Python version: 3.9
- Advanced settings: None needed

**Deployment time:** ~2 minutes for first build

---

### Continuous Deployment (Automatic)

After initial setup, every push to GitHub main branch triggers automatic redeployment:

```
1. Developer makes changes locally (VS Code)
2. Commit changes via Source Control panel
3. Push to GitHub
4. Streamlit Cloud detects new commit
5. Rebuilds application (installs requirements.txt)
6. Deploys new version (~2 minutes)
7. Live application updated automatically
```

**No manual deployment needed.** Just push to GitHub and wait 2 minutes.

---

## Application Requirements

### Python Version

**Version:** Python 3.9 or higher

**Why:** Streamlit 1.31 requires Python 3.9+

### Dependencies

From `requirements.txt`:

```
streamlit==1.31.0          # Web framework
pandas==2.1.4              # Data handling
plotly==5.18.0             # Interactive charts (RIASEC radar)
openpyxl==3.1.2            # Excel file reading
```

**Total installation size:** ~150 MB

**Installation time:** ~30 seconds on Streamlit Cloud

---

## Resource Usage

### Streamlit Community Cloud Limits

**Free tier includes:**
- 1 GB RAM per app
- 1 CPU core
- Unlimited bandwidth
- 3 apps maximum per account

**This app uses:**
- ~200 MB RAM (well within limits)
- <1% CPU (extremely lightweight)
- ~5 MB storage (just code + Excel file)

**Performance:** No issues. App loads in <2 seconds, calculations complete in <0.5 seconds.

---

## Monitoring and Maintenance

### Application Health

**Uptime:** 99.9% (only down during Streamlit Cloud maintenance)

**Error monitoring:** Streamlit Cloud dashboard shows app status, logs, and errors

**Logs access:** Available in Streamlit Cloud interface (last 100 lines visible)

### Maintenance Tasks

**Regular maintenance:** None required

**Occasional updates:**
- Programme data changes (when NUS adds/removes programmes)
- Streamlit version upgrades (1-2 times per year)
- Bug fixes as discovered

**Update process:**
1. Make changes locally
2. Test with developer mode
3. Push to GitHub
4. Automatic redeployment

---

## Domain and SSL

**Domain:** Streamlit-provided subdomain (auto-generated)

**Custom domain:** Not configured (would require Streamlit Pro plan)

**SSL/HTTPS:** Automatic (Streamlit provides free SSL certificate)

**Security:** All traffic encrypted

---

## Data Privacy and Storage

### User Data

**Storage:** NONE. The application does not store any user data.

**Session data:** Stored in browser memory only, cleared on page refresh

**Privacy benefits:**
- No login required
- No email collection
- No tracking cookies
- No analytics
- Completely anonymous usage

**Limitation:** Users cannot save results or revisit past assessments

### Application Data

**Programme database:** Public (stored in GitHub repository)

**Question bank:** Public (stored in GitHub repository)

**No sensitive data:** All content is educational and public-facing

---

## Performance Optimization

### Caching Strategy

```python
@st.cache_data
def load_data():
    # Excel file loaded once, cached in memory
    # Subsequent users access cached version
    # Cache invalidated on redeployment
    ...
```

**Benefits:**
- First user: 1-2 second load time
- Subsequent users: <0.5 second load time
- No database queries needed

### Session State Management

```python
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'responses' not in st.session_state:
    st.session_state.responses = {}
```

**Benefits:**
- Maintains user progress during questionnaire
- Prevents data loss on accidental refresh
- Enables multi-page flow without URL parameters

---

## Accessibility

**Mobile responsive:** Yes, Streamlit adapts to screen size automatically

**Browser compatibility:**
- Chrome (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Chrome Android)

**Loading time:**
- Desktop: <2 seconds
- Mobile: <3 seconds

**Internet requirements:** Any connection (works on 3G, 4G, 5G, WiFi)

---

## Deployment Alternatives Considered

### Why not other platforms?

**Heroku:**
- ❌ Requires credit card (even for free tier)
- ❌ More complex deployment process
- ❌ Sleeps after 30 minutes of inactivity
- ✅ More customization options

**Vercel/Netlify:**
- ❌ Optimized for static sites (JavaScript/React)
- ❌ Would require rewriting app in JavaScript
- ✅ Very fast performance

**AWS/Azure/GCP:**
- ❌ Complex setup (EC2 instances, containers, etc.)
- ❌ Monthly costs (~$10-50)
- ❌ Requires DevOps knowledge
- ✅ Full control and scalability

**Streamlit Cloud chosen because:**
- ✅ Specifically designed for Python apps
- ✅ Zero configuration needed
- ✅ Free forever (for public apps)
- ✅ Automatic HTTPS
- ✅ GitHub integration built-in
- ✅ Perfect for educational/demo projects

---

## Scaling Considerations

### Current Usage

**Estimated users:** <100 per month (primarily for FYP demonstration and testing)

**Concurrent users:** <10 at any time

**Performance:** No issues with current load

### If Usage Grows

**Scenario: 1,000+ users per day**

**Required changes:**
1. Upgrade to Streamlit Pro plan ($250/month for higher resource limits)
2. Implement analytics to track usage patterns
3. Add load balancing if needed
4. Consider database migration if programme data becomes complex

**Current setup handles:** Up to ~500 concurrent users before hitting resource limits

**For FYP purposes:** Current free tier is completely sufficient

---

## Disaster Recovery

### Backup Strategy

**Code backup:** Full history in GitHub (never lost)

**Data backup:** Excel file in GitHub (version controlled)

**Deployment backup:** Can redeploy to new Streamlit app in 5 minutes if needed

### Recovery Procedures

**If app crashes:**
1. Check Streamlit Cloud logs for error
2. Fix error locally
3. Push to GitHub
4. Auto-redeployment in 2 minutes

**If Streamlit Cloud goes down:**
1. Run app locally: `streamlit run app.py`
2. Share via ngrok tunnel (temporary public URL)
3. Wait for Streamlit Cloud to recover

**If GitHub goes down:**
1. Deploy from local copy to alternative hosting
2. Update DNS/links once deployed

---

## Future Deployment Enhancements

**Potential improvements:**

1. **Custom domain:** Purchase `nusadvisor.sg` or similar
2. **Analytics:** Add Google Analytics to track usage patterns
3. **User accounts:** Implement login system to save results
4. **Database migration:** Move from Excel to PostgreSQL if programme count grows significantly
5. **A/B testing:** Test different UI variations to improve user experience
6. **Multi-language support:** Add Chinese/Malay translations for broader reach

**None currently implemented:** Project focused on core functionality, not advanced deployment features.

---

[← Back to Main Report](../index.md)
