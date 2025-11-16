import uuid
import httpx

from fastapi import APIRouter, Response, Request, Cookie, HTTPException
from fastapi.responses import RedirectResponse

from account.adapter.input.web.account_router import create_account
from account.adapter.input.web.request.create_account_request import CreateAccountRequest
from config.redis_config import get_redis
from social_oauth.application.usecase.google_oauth2_usecase import GoogleOAuth2UseCase
from social_oauth.infrastructure.service.google_oauth2_service import GoogleOAuth2Service

authentication_router = APIRouter()
service = GoogleOAuth2Service()
usecase = GoogleOAuth2UseCase(service)
redis_client = get_redis()

GOOGLE_USERINFO_URI = "https://www.googleapis.com/oauth2/v3/userinfo"


@authentication_router.get("/google")
async def redirect_to_google():
    url = usecase.get_authorization_url()
    print("[DEBUG] Redirecting to Google:", url)
    return RedirectResponse(url)


@authentication_router.get("/google/redirect")
async def process_google_redirect(
        response: Response,
        code: str,
        state: str | None = None
):
    print("[DEBUG] /google/redirect called")

    # code -> access token
    access_token = usecase.login_and_fetch_user(state or "", code)
    r = httpx.get("https://oauth2.googleapis.com/tokeninfo", params={"access_token": access_token.access_token})
    print(r.status_code, r.text)

    # access token으로 유저 정보 요청
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                GOOGLE_USERINFO_URI,
                headers={"Authorization": f"Bearer {access_token.access_token}"},
                timeout=10.0
            )

        print("[DEBUG] Google user info request response:", res)
        if res.status_code != 200:
            print("[WARN] Failed to retrieve Google user info:", res.status_code)
            raise HTTPException(status_code=400, detail="Failed to retrieve Google user info")

        userinfo = res.json()
        print("[DEBUG] Google user info:", userinfo)

        # sub(id) 추출
        google_id = userinfo.get("sub")

        if not google_id:
            raise HTTPException(status_code=400, detail="Google 'sub' field missing")

        print("[DEBUG] Google user id(sub):", google_id)

    except Exception as e:
        print("[ERROR] Exception during Google user info retrieval:", e)
        raise HTTPException(status_code=500, detail="Exception during Google user info retrieval")

    finally:
        await client.aclose()

    print("[DEBUG] Google user info retrieved successfully")

    # session_id 생성
    session_id = str(uuid.uuid4())
    print("[DEBUG] Generated session_id:", session_id)

    # userId(oauth_id)에 일치하는 account 있는지 확인 한다.

    # Create a new account using the retrieved user info
    account = await create_account(
        request=CreateAccountRequest(
            user_uuid=session_id,
            oauth_id=google_id,
            oauth_type="GOOGLE",
            nickname="",
            name=userinfo.get("name"),
            profile_image=userinfo.get("picture"),
            email=userinfo.get("email"),
            phone_number="",
            active_status="Y",
            role_id=""
        )
    )

    print("[DEBUG] Account created:", account)

    # Redis에 session 저장 (1시간 TTL)
    redis_client.set(session_id, access_token.access_token, ex=3600)
    print("[DEBUG] Session saved in Redis:", redis_client.exists(session_id))

    # 브라우저 쿠키 발급
    redirect_response = RedirectResponse("http://localhost:3000")
    redirect_response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=False,
        samesite="none",
        max_age=3600
    )
    print("[DEBUG] Cookie set in RedirectResponse directly")
    return redirect_response


@authentication_router.get("/status")
async def auth_status(request: Request, session_id: str | None = Cookie(None)):
    print("[DEBUG] /status called")

    # 모든 요청 헤더 출력
    print("[DEBUG] Request headers:", request.headers)

    # 쿠키 확인
    print("[DEBUG] Received session_id cookie:", session_id)

    if not session_id:
        print("[DEBUG] No session_id received. Returning logged_in: False")
        return {"logged_in": False}

    exists = redis_client.exists(session_id)
    print("[DEBUG] Redis has session_id?", exists)

    return {"logged_in": bool(exists)}
