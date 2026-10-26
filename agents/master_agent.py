import json
import datetime
from typing import Dict
from agents.fundamental_agent import FundamentalAgent
from agents.smc_agent import SMCAgent
from ai_brain.inference_memory import InferenceMemoryEngine
from data_engine.macro_historical_engine import MacroHistoricalEngine
from data_engine.bond_spread_engine import BondSpreadEngine
from data_engine.commodity_correlation_engine import CommodityCorrelationEngine
from data_engine.risk_regime_engine import RiskRegimeEngine
from data_engine.real_rates_engine import RealRatesEngine
from data_engine.net_liquidity_engine import NetLiquidityEngine
from data_engine.pmi_engine import PMIEngine
from data_engine.central_bank_nlp_engine import CentralBankNLPEngine

class MasterInstitutionalAgent:
    def __init__(self):
        self.fundamental_agent = FundamentalAgent()
        self.smc_agent = SMCAgent()
        self.memory_engine = InferenceMemoryEngine()
        self.macro_engine = MacroHistoricalEngine()
        self.bond_engine = BondSpreadEngine()
        self.commodity_engine = CommodityCorrelationEngine()
        self.risk_engine = RiskRegimeEngine()
        self.real_rates_engine = RealRatesEngine()
        self.liquidity_engine = NetLiquidityEngine()
        self.pmi_engine = PMIEngine()
        self.nlp_engine = CentralBankNLPEngine()

    def synthesize_market_analysis(self, currency_pair: str) -> Dict:
        fund_report = self.fundamental_agent.evaluate_fundamentals(currency_pair)
        timeframe_trends = self.smc_agent.analyze_multi_timeframe_trend(currency_pair)
        smc_4h = self.smc_agent.detect_smc_structures(currency_pair, "4h")
        
        current_date = datetime.datetime.now()
        macro_analysis = self.macro_engine.get_macro_score(currency_pair, current_date)
        bond_analysis = self.bond_engine.get_bond_spread_analysis(currency_pair)
        commodity_analysis = self.commodity_engine.analyze_commodity_impact(currency_pair)
        risk_analysis = self.risk_engine.get_market_risk_regime()
        real_rates = self.real_rates_engine.get_real_interest_rates()
        liquidity = self.liquidity_engine.get_net_liquidity_status()
        pmi = self.pmi_engine.get_pmi_analysis(currency_pair)
        nlp = self.nlp_engine.analyze_central_bank_tone(currency_pair)
        
        risk_regime = risk_analysis.get('regime', 'Neutral')
        
        general_action = "🟢 فرصة شراء قوية (Strong Buy Opportunity)"
        if "Risk-Off" in risk_regime:
            general_action = "🟡 حياد / ترقب بحذر (Stand Aside)"
        elif "انكماش" in pmi.get('bias', ''):
            general_action = "🔴 فرصة بيع قوية (Strong Sell Opportunity)"

        # تخصيص وصف الفائدة بناءً على زوج العملات
        rate_val = real_rates.get('real_rate', 0)
        if "JPY" in currency_pair:
            rate_desc = f"الفائدة الحقيقية الأمريكية مقابل الين عند {rate_val}%. اتساع الفارق يدعم الضغط على الين."
        elif "XAU" in currency_pair:
            rate_desc = f"الفائدة الحقيقية عند {rate_val}%. المستويات الحالية تضغط على الذهب وتزيد جاذبية السندات."
        elif "EUR" in currency_pair:
            rate_desc = f"فارق الفائدة الحقيقية بين الفيدرالي والمركزي الأوروبي عند {rate_val}%."
        else:
            rate_desc = f"الفائدة الحقيقية وسندات الدين عند {rate_val}%."

        comprehensive_context = {
            "target_pair": currency_pair,
            "general_action": general_action,
            "macro_analysis": macro_analysis,
            "risk_analysis": risk_analysis,
            "real_rates_desc": rate_desc,
            "liquidity": liquidity,
            "pmi": pmi,
            "nlp": nlp,
            "smc_structures": smc_4h
        }
        return comprehensive_context

    def generate_dual_layer_report(self, currency_pair: str) -> dict:
        context = self.synthesize_market_analysis(currency_pair)
        
        action = context.get('general_action', '')
        risk_desc = context.get('risk_analysis', {}).get('description', '')
        
        layman_summary = f"""
🎯 الخلاصة المبسطة للمستخدم:
- التوصية العامة: {action}
- حالة السوق بكلمات بسيطة: {risk_desc}
- نصيحة المنظومة: الالتزام التام بالاتجاه المدعوم بالسيولة والماكرو.
        """.strip()

        smc = context['smc_structures']
        price = smc.get('current_market_price', 0)
        pools = smc.get('high_liquidity_pools', {})
        blocks = smc.get('dynamic_order_blocks', {})

        buy_pool = pools.get('buy_side_liquidity_target', 'غير متوفر')
        sell_pool = pools.get('sell_side_liquidity_target', 'غير متوفر')
        demand = blocks.get('bullish_demand_zone', 'غير متوفر')
        supply = blocks.get('bearish_supply_zone', 'غير متوفر')

        institutional_report = f"""
🏛️ التقرير الاحترافي الكمي المتقدم ({currency_pair}):
- السعر الحالي: {price}
- تجمعات السيولة العالية (Liquidity Pools): شراء: {buy_pool} | بيع: {sell_pool}
- مناطق الطلب والعرض (SMC Zones): طلب: {demand} | عرض: {supply}
- نبرة البنك المركزي (NLP): {context.get('nlp', {}).get('tone')}
- الفائدة الحقيقية والسيولة: {context.get('real_rates_desc')}
        """.strip()

        return {
            "layman_view": layman_summary,
            "institutional_view": institutional_report,
            "raw_data": context
        }
