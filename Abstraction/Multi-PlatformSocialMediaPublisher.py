#06-07-2026
#Multi-Platform Social Media Publisher
from abc import ABC,abstractmethod
from datetime import datetime
import time
import math
import re
import hashlib
import datetime
from typing import List,Dict,Any,Optional

class PublisherException(Exception):
    def __init__(self, message:str,platform_name:str):
        super().__init__(f"[{platform_name.upper()}] {message}")
        self.platform_name=platform_name
        self.timestamp=datetime.now()

class AuthenticationError(PublisherException):
    pass

class ContentValidationError(PublisherException):
    pass

class RateLimitExceededError(PublisherException):
    pass

class PostPayLoad:
    def __init__(self,text: str, media_url: Optional[str] = None, media_type: Optional[str] = None):
        self.text = text
        self.media_url = media_url
        self.media_type = media_type  # Expected options: 'IMAGE', 'VIDEO', or None
        self.payload_id = hashlib.md5(f"{text}{media_url}{time.time()}".encode()).hexdigest()[:8]

class PublicationReport:
    def __init__(self, platform: str, success: bool, tracking_id: Optional[str] = None, error_msg: Optional[str] = None):
        self.platform = platform
        self.success = success
        self.tracking_id = tracking_id
        self.error_message = error_msg
        self.timestamp = datetime.datetime.utcnow()

class SocialMediaPlatform(ABC):
    global_total_attempts: int = 0
    global_successful_posts: int = 0
    def __init__(self,platform_name: str, api_version: str, api_key: str, api_secret: str):
        self._platform_name=platform_name
        self._api_version=api_version
        self._is_authenticated=False

        self.__api_key=api_key
        self.__api_secret=api_secret
        self.__connection_token:Optional[str]=None
    @property
    def platform_name(self)->str:
        return self._platform_name
    @property
    def is_authenticated(self)->bool:
        return self._is_authenticated
    
    @classmethod
    def increment_global_success(cls)->None:
        cls.global_successful_posts+=1
    
    @classmethod
    def increment_global_attempts(cls)->None:
        cls.global_total_attempts+=1
    
    @staticmethod
    def _sanitize(text:str)->str:
        if not text:
            return ""
        return " ".join(text.split())
    
    def initialize_connection(self)->bool:
        SocialMediaPlatform.increment_global_attempts()
        raw_signature = f"{self.__api_key}:{self.__api_secret}:{self._api_version}"
        self.__connection_token=hashlib.sha256(raw_signature.encode()).hexdigest()
        try:
            
            return self._is_authenticated
        except Exception as err:
            self._is_authenticated=False
            raise AuthenticationError(f"Authentication phase critical failure: {str(err)}", self._platform_name)
    
    @abstractmethod
    def authenticate(self,secure_token:str)->bool:
        pass
    @abstractmethod
    def validate_content(self,payload:PostPayLoad)->bool:
        pass
    @abstractmethod
    def execute_publish(self,payload:PostPayLoad)->str:
        pass

class TwitterPlatform(SocialMediaPlatform):
    CHARACTER_LIMIT: int = 280
    ALLOWED_MEDIA_TYPES: List[str] = ["IMAGE", "VIDEO"]
    def __init__(self, api_key: str, api_secret: str, handle: str):
        super().__init__(platform_name="Twitter", api_version="v2.0", api_key=api_key, api_secret=api_secret)
        self.handle=handle
        self._local_post_history:List[str]=[]
    
    def authenticate(self, secure_token:str)->bool:
        if len(secure_token)==64 and self.handle.startswith("@"):
            return True
        return False
    
    def validate_content(self, payload:PostPayLoad)->bool:
        sanitized=self._sanitize(payload.text)
        if len(sanitized)>self.CHARACTER_LIMIT:
            raise ContentValidationError(f"Content size ({len(sanitized)} chars) breaks limits ({self.CHARACTER_LIMIT} chars).", self._platform_name)
        if payload.media_type and payload.media_type not in self.ALLOWED_MEDIA_TYPES:
            raise ContentValidationError(
                f"Media format '{payload.media_type}' is unsupported on standard feeds.", 
                self._platform_name
            )
        return True
    
    def execute_publish(self, payload:PostPayLoad)->bool:
        if not self.is_authenticated:
            raise AuthenticationError("Cannot deploy content. Session unauthenticated.", self._platform_name)
        self.validate_content(payload)
        simulated_id = f"TW-PR-{hashlib.md5(payload.payload_id.encode()).hexdigest()[:12]}"
        self._local_post_history.append(simulated_id)
        self.increment_global_success()
        return simulated_id

class LinkedInPlatform(SocialMediaPlatform):
    CHARACTER_LIMIT: int = 3000
    MANDATORY_PROFESSIONAL_KEYWORDS: List[str] = ["#career", "#tech", "#business", "#growth", "#innovation", "#work"]

    def __init__(self, api_key: str, api_secret: str, company_urn: str):
        super().__init__(platform_name="LinkedIn", api_version="v3", api_key=api_key, api_secret=api_secret)
        self.company_urn:str=company_urn
        self._strict_policy_mode:bool=True
    
    def authenticate(self, secure_token: str) -> bool:
        if "urn:li:organization:" in self.company_urn:
            return True
        return False
    
    def validate_content(self, payload: PostPayLoad) -> bool:
        sanitized=self._sanitize(payload.text)
        if len(sanitized)>self.CHARACTER_LIMIT:
            raise ContentValidationError("Corporate statement length exceeds limits.", self._platform_name)
        if len(sanitized) < 10:
            raise ContentValidationError("Corporate statement length exceeds limits.", self._platform_name)
        if self._strict_policy_mode:
            has=any(tag in sanitized.lower() for tag in self.MANDATORY_PROFESSIONAL_KEYWORDS)
            if not has:
                raise ContentValidationError(
                    "Post rejected. Compliance rules require at least one industry anchor hashtag.", 
                    self._platform_name
                )
        return True
    
    def execute_publish(self, payload: PostPayLoad) -> str:
        if not self.is_authenticated:
            raise AuthenticationError("Active LinkedIn context validation context missing.", self._platform_name)
        self.validate_content(payload)
        simulated_id = f"LI-URN-{uuid_mock(payload.text)}"
        self.increment_global_success()
        return simulated_id

class InstagramPlatform(SocialMediaPlatform):
    """Instagram integration demanding visual context payloads."""

    HASHTAG_LIMIT: int = 30

    def __init__(self, api_key: str, api_secret: str, profile_id: str):
        super().__init__(platform_name="Instagram", api_version="v14.0", api_key=api_key, api_secret=api_secret)
        self.profile_id: str = profile_id

    def authenticate(self, secure_token: str) -> bool:
        return len(self.profile_id) == 10 and self.profile_id.isdigit()

    def validate_content(self, payload: PostPayLoad) -> bool:
        # Business Logic Constraint: Instagram MUST contain a valid media item
        if not payload.media_url or payload.media_type != "IMAGE":
            raise ContentValidationError("Instagram requires an asset image payload attachment.", self._platform_name)
            
        sanitized = self._sanitize_text(payload.text)
        hashtags = re.findall(r"#\w+", sanitized)
        
        if len(hashtags) > self.HASHTAG_LIMIT:
            raise ContentValidationError(
                f"Hashtag count ({len(hashtags)}) exceeds allowed limit ({self.HASHTAG_LIMIT}).", 
                self._platform_name
            )
        return True

    def execute_publish(self, payload: PostPayLoad) -> str:
        if not self.is_authenticated:
            raise AuthenticationError("Graph API session state invalid.", self._platform_name)
            
        self.validate_content(payload)
        
        simulated_id = f"IG-MEDIA-{hashlib.sha1(payload.media_url.encode()).hexdigest()[:10]}"
        self.increment_global_success()
        return simulated_id

def uuid_mock(seed: str) -> str:
    return hashlib.md5(seed.encode()).hexdigest()[:8]

class MultiPlatformPublisher:
    """
    The main coordinator engine. It relies purely on the abstract base 
    interface, remaining completely agnostic to specific subclass internal systems.
    """
    MAX_RETRY_ATTEMPTS: int = 3

    def __init__(self):
        # Master platform registry map
        self.__registered_platforms: Dict[str, SocialMediaPlatform] = {}
        self.__system_logs: List[Dict[str, Any]] = []

    def register_platform(self, platform: SocialMediaPlatform) -> None:
        """Registers a platform implementation, triggering immediate initialization."""
        print(f"[ENGINE] Connecting channel target: {platform.platform_name}...")
        try:
            if platform.initialize_connection():
                self.__registered_platforms[platform.platform_name.lower()] = platform
                self._log_event("REGISTRATION_SUCCESS", f"Channel {platform.platform_name} active.")
            else:
                self._log_event("REGISTRATION_FAIL", f"Channel validation failure: {platform.platform_name}")
        except PublisherException as ex:
            self._log_event("REGISTRATION_CRITICAL", f"Failed registration routine. Error: {str(ex)}")

    def remove_platform(self, platform_name: str) -> bool:
        """Removes a platform from active distribution pools."""
        target = platform_name.lower()
        if target in self.__registered_platforms:
            del self.__registered_platforms[target]
            self._log_event("DEREGISTRATION", f"Channel {platform_name} removed.")
            return True
        return False

    def _log_event(self, context: str, note: str) -> None:
        """Internal protected logger keeping clean tracking states."""
        self.__system_logs.append({
            "timestamp": datetime.datetime.utcnow(),
            "context": context,
            "message": note
        })

    def get_active_channels(self) -> List[str]:
        """Returns clean list string lookups of initialized adapters."""
        return [p.platform_name for p in self.__registered_platforms.values()]

    def broadcast_post(self, payload: PostPayLoad) -> List[PublicationReport]:
        """
        Executes unified publication across all registered platform frameworks.
        Includes built-in validation preprocessing and granular error recovery strategies.
        """
        reports: List[PublicationReport] = []
        
        if not self.__registered_platforms:
            self._log_event("BROADCAST_EMPTY", "Broadcast triggered without active distribution channels.")
            return reports

        self._log_event("BROADCAST_START", f"Processing Payload ID {payload.payload_id}")

        for label, platform in self.__registered_platforms.items():
            attempt = 0
            success_status = False
            error_details: Optional[str] = None
            remote_id: Optional[str] = None

            # Retry loop matching infrastructure failure tolerances
            while attempt < self.MAX_RETRY_ATTEMPTS and not success_status:
                attempt += 1
                try:
                    # Polling the abstract interface methods safely
                    remote_id = platform.execute_publish(payload)
                    success_status = True
                    error_details = None
                except ContentValidationError as cve:
                    # Content errors fail immediately; retries will not resolve schema issues
                    error_details = f"Validation Error: {str(cve)}"
                    break
                except AuthenticationError as ae:
                    error_details = f"Auth Context Corrupted: {str(ae)}"
                    # Trigger connection re-initialization try
                    try:
                        platform.initialize_connection()
                    except PublisherException:
                        break
                except Exception as critical_err:
                    error_details = f"Unhandled Exception (Attempt {attempt}): {str(critical_err)}"
                    time.sleep(0.01)  # Micro sleep simulating backoff delay blocks

            # Document outcomes into metrics storage
            report = PublicationReport(
                platform=platform.platform_name,
                success=success_status,
                tracking_id=remote_id,
                error_msg=error_details
            )
            reports.append(report)
            
            outcome_text = f"SUCCESS ID: {remote_id}" if success_status else f"FAILED: {error_details}"
            self._log_event("PLATFORM_OUTCOME", f"Platform {platform.platform_name} completed with {outcome_text}")

        return reports

    def export_telemetry_summary(self) -> Dict[str, Any]:
        """Compiles global runtime metric diagnostics."""
        return {
            "monitored_channels_count": len(self.__registered_platforms),
            "framework_total_connection_attempts": SocialMediaPlatform.global_total_attempts,
            "framework_global_successful_posts": SocialMediaPlatform.global_successful_posts,
            "total_system_logged_events": len(self.__system_logs)
        }


# ==========================================
# LAYER 6: SIMULATION AND VERIFICATION VERIFIERS
# ==========================================

if __name__ == "__main__":
    print("=== INITIALIZING ABSTRACTION ENGINE TESTING PIPELINE ===")
    
    # 1. Instantiate the central application broker
    engine = MultiPlatformPublisher()

    # 2. Instantiate concrete implementations containing unique business requirements
    tw_channel = TwitterPlatform(api_key="TW_KEY_123", api_secret="SEC_456", handle="@TechUpdates")
    li_channel = LinkedInPlatform(api_key="LI_KEY_987", api_secret="SEC_321", company_urn="urn:li:organization:9999")
    ig_channel = InstagramPlatform(api_key="IG_KEY_555", api_secret="SEC_888", profile_id="1234567890")

    print("\n--- Phase 1: Registering Subclasses via Abstract Interfaces ---")
    engine.register_platform(tw_channel)
    engine.register_platform(li_channel)
    engine.register_platform(ig_channel)

    print(f"Active Channels: {engine.get_active_channels()}")

    print("\n--- Phase 2: Processing Content Payload 1 (Compliant text, missing image) ---")
    # This payload should satisfy Twitter and LinkedIn, but fail on Instagram due to asset constraints.
    payload_one = PostPayLoad(
        text="Exploring advanced architectural patterns in Python! #Tech system designs look great using OOP abstraction."
    )
    
    results = engine.broadcast_post(payload_one)
    for r in results:
        status = "PASSED" if r.success else "FAILED"
        print(f" -> Platform: {r.platform} | Result: {status} | Info/ID: {r.tracking_id or r.error_message}")

    print("\n--- Phase 3: Processing Content Payload 2 (Valid LinkedIn/Twitter text + Visual Asset) ---")
    # This payload satisfies Instagram, but fails LinkedIn rules if we exceed constraints or omit professional hashtags.
    # Let's verify standard image deployment with valid matching structures.
    payload_two = PostPayLoad(
        text="Scaling content delivery loops seamlessly across global regions. #Innovation at scale.",
        media_url="https://assets.storage.net/images/diagram.png",
        media_type="IMAGE"
    )

    results_two = engine.broadcast_post(payload_two)
    for r in results_two:
        status = "PASSED" if r.success else "FAILED"
        print(f" -> Platform: {r.platform} | Result: {status} | Info/ID: {r.tracking_id or r.error_message}")

    print("\n--- Phase 4: Processing Content Payload 3 (Violating Twitter Maximum Rules) ---")
    # Generating an excessively long text string to force validation failures on Twitter limits.
    oversized_text = "Enforcing long text validation. " * 15 + " #Business growth strategies."
    payload_three = PostPayLoad(text=oversized_text)

    results_three = engine.broadcast_post(payload_three)
    for r in results_three:
        status = "PASSED" if r.success else "FAILED"
        print(f" -> Platform: {r.platform} | Result: {status} | Info/ID: {r.tracking_id or r.error_message}")

    print("\n--- Phase 5: Diagnostic Engine Metrics Tracking Overview ---")
    metrics = engine.export_telemetry_summary()
    for key, val in metrics.items():
        print(f" {key.replace('_', ' ').title()}: {val}")
        
    print("\n=== SYSTEM VERIFICATION RUN COMPLETED SUCCESSFULLY ===")