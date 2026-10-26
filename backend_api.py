from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agents.master_agent import MasterInstitutionalAgent

app = FastAPI(
    title="Global Macro Quant API",
    version="2.0",
    description="الخادم السحابي المؤسسي لنظام التداول الكمي المدمج بالماكرو والسيولة وريجيم المخاطر"
)

# السماح بالاتصال من أي واجهة خارجية أو تطبيق موبايل
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = MasterInstitutionalAgent()

@app.get("/")
def home():
    return {"status": "Active", "message": "مرحباً بك في الخادم الخلفي لنظام التداول المؤسسي!"}

@app.get("/analyze/{currency_pair}")
def analyze_market(currency_pair: str):
    """
    جلب التحليل الشامل والقرار الاستراتيجي لأي زوج عملات أو أصل (مثل EUR/USD أو XAU/USD)
    """
    try:
        # تنسيق اسم الأصل
        formatted_pair = currency_pair.upper().replace("-", "/")
        if "/" not in formatted_pair and len(formatted_pair) == 6:
            formatted_pair = f"{formatted_pair[:3]}/{formatted_pair[3:]}"
            
        context = agent.synthesize_market_analysis(formatted_pair)
        report = agent.generate_local_ai_decision(formatted_pair)
        
        return {
            "success": True,
            "currency_pair": formatted_pair,
            "institutional_report": report,
            "raw_data": context
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
