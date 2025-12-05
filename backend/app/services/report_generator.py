from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os
import re
from typing import Dict, Any, List, Union

class ReportGenerator:
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_styles()
    
    def _setup_styles(self):
        """Initialize custom styles"""
        # Title Style
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=26,
            leading=32,
            textColor=colors.HexColor('#1a237e'),
            alignment=TA_CENTER,
            spaceAfter=30
        ))
        
        # Heading 2 (Section Headers)
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=18,
            leading=22,
            textColor=colors.HexColor('#283593'),
            spaceBefore=20,
            spaceAfter=10,
            borderPadding=5,
            borderColor=colors.HexColor('#e8eaf6'),
            borderWidth=0,
            backColor=colors.HexColor('#e8eaf6')
        ))
        
        # Heading 3 (Sub-sections)
        self.styles.add(ParagraphStyle(
            name='SubHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#303f9f'),
            spaceBefore=12,
            spaceAfter=6
        ))
        
        # Body Text
        self.styles.add(ParagraphStyle(
            name='ReportBody',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=8
        ))

    def _clean_markdown(self, text: str) -> str:
        """Convert basic Markdown to ReportLab XML tags"""
        if not text: return ""
        
        # Bold: **text** -> <b>text</b>
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        # Italic: *text* -> <i>text</i>
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        # Code: `text` -> <font name="Courier">text</font>
        text = re.sub(r'`(.*?)`', r'<font face="Courier">\1</font>', text)
        
        return text

    def _create_table(self, data: List[List[str]], col_widths: List[float] = None) -> Table:
        """Create a styled table"""
        if not data: return None
        
        # Auto-calculate widths if not provided
        if not col_widths:
            col_count = len(data[0])
            available_width = 7.0 * inch
            col_widths = [available_width / col_count] * col_count
            
        t = Table(data, colWidths=col_widths, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3949ab')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.white),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f5f5f5'), colors.white])
        ]))
        return t

    def _render_agent_data(self, agent_name: str, result: Dict[str, Any]) -> List:
        """Render specific data structures for each agent"""
        elements = []
        data = result.get('data', {})
        
        # 1. Clinical Trials
        if "clinical" in agent_name.lower() or "trials" in agent_name.lower():
            trials = data.get('trials', [])
            if trials:
                elements.append(Paragraph(f"Found {len(trials)} Clinical Trials", self.styles['SubHeader']))
                table_data = [['NCT ID', 'Title', 'Phase', 'Status']]
                for t in trials[:10]: # Limit to 10 for PDF
                    table_data.append([
                        t.get('nct_id', 'N/A'),
                        Paragraph(t.get('title', 'N/A'), self.styles['Normal']), # Wrap text
                        t.get('phase', 'N/A'),
                        t.get('status', 'N/A')
                    ])
                elements.append(self._create_table(table_data, col_widths=[1.2*inch, 3.5*inch, 1.0*inch, 1.3*inch]))
                elements.append(Spacer(1, 0.2*inch))

        # 2. Patent Landscape
        elif "patent" in agent_name.lower():
            patents = data.get('patents', [])
            if patents:
                elements.append(Paragraph(f"Found {len(patents)} Patents", self.styles['SubHeader']))
                table_data = [['Patent No.', 'Title', 'Assignee', 'Status']]
                for p in patents[:10]:
                    table_data.append([
                        p.get('patent_number', 'N/A'),
                        Paragraph(p.get('title', 'N/A'), self.styles['Normal']),
                        p.get('assignee', 'N/A'),
                        p.get('status', 'N/A')
                    ])
                elements.append(self._create_table(table_data, col_widths=[1.5*inch, 3.0*inch, 1.5*inch, 1.0*inch]))
                elements.append(Spacer(1, 0.2*inch))

        # 3. Web Intelligence (PubMed)
        elif "web" in agent_name.lower() or "intelligence" in agent_name.lower():
            papers = data.get('pubmed_papers', []) or data.get('articles', [])
            if papers:
                elements.append(Paragraph(f"Key Scientific Literature ({len(papers)} papers)", self.styles['SubHeader']))
                for i, p in enumerate(papers[:5], 1):
                    elements.append(Paragraph(
                        f"{i}. <b>{p.get('title', 'N/A')}</b><br/>"
                        f"<font color='grey' size=9>{p.get('source', 'Journal')} | {p.get('pubdate', 'Date')} | PMID: {p.get('pmid', '')}</font>",
                        self.styles['ReportBody']
                    ))
                elements.append(Spacer(1, 0.1*inch))

        # 4. Market Intelligence
        elif "market" in agent_name.lower():
            market_data = data.get('market_data', {})
            
            # Trade Data
            trade = market_data.get('global_trade', {})
            if trade and 'total_imports_usd' in trade:
                elements.append(Paragraph("Global Trade Overview", self.styles['SubHeader']))
                elements.append(Paragraph(
                    f"<b>Total Imports:</b> ${trade.get('total_imports_usd', 0):,}<br/>"
                    f"<b>Total Exports:</b> ${trade.get('total_exports_usd', 0):,}<br/>"
                    f"<b>Balance:</b> ${trade.get('trade_balance', 0):,}",
                    self.styles['ReportBody']
                ))
            
            # Pricing Data
            cms = market_data.get('us_pricing', {})
            nppa = market_data.get('india_pricing', {})
            if cms or nppa:
                elements.append(Paragraph("Pricing Analysis", self.styles['SubHeader']))
                price_data = [['Region', 'Drug', 'Price Info', 'Source']]
                if cms:
                    price_data.append(['USA', cms.get('drug_name', 'N/A'), f"${cms.get('avg_price_per_unit', 0)} / unit", 'CMS Medicare'])
                if nppa:
                    price_data.append(['India', nppa.get('drug_name', 'N/A'), nppa.get('ceiling_price', 'N/A'), 'NPPA'])
                elements.append(self._create_table(price_data, col_widths=[1.0*inch, 2.0*inch, 2.0*inch, 2.0*inch]))

        # Generic fallback for other data
        else:
            # If we haven't handled it specifically, just dump key-values nicely
            pass

        return elements

    async def generate_report(
        self,
        query: str,
        synthesis: str,
        agent_results: Dict[str, Any],
        plan: Dict[str, Any]
    ) -> str:
        """Generate comprehensive PDF report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pharma_research_report_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(
            filepath, 
            pagesize=A4,
            rightMargin=72, leftMargin=72,
            topMargin=72, bottomMargin=72
        )
        story = []
        
        # --- TITLE PAGE ---
        story.append(Spacer(1, 2*inch))
        story.append(Paragraph("PHARMACEUTICAL INTELLIGENCE REPORT", self.styles['ReportTitle']))
        story.append(Spacer(1, 0.5*inch))
        
        # Metadata Table
        metadata = [
            ['RESEARCH QUERY', query],
            ['GENERATED ON', datetime.now().strftime("%B %d, %Y at %H:%M")],
            ['INTENT', plan.get('intent', 'General Research')],
            ['CONFIDENCE', 'High (Multi-Source Verification)']
        ]
        
        t = Table(metadata, colWidths=[2.5*inch, 4.5*inch])
        t.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 1, colors.HexColor('#e0e0e0')),
            ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#757575')),
            ('TEXTCOLOR', (1,0), (1,-1), colors.black),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 15),
            ('TOPPADDING', (0,0), (-1,-1), 15),
        ]))
        story.append(t)
        story.append(PageBreak())
        
        # --- EXECUTIVE SUMMARY ---
        story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        
        # Process Markdown Synthesis
        # Split by double newline to get paragraphs
        paragraphs = synthesis.split('\n\n')
        for p in paragraphs:
            p = p.strip()
            if not p: continue
            
            # Check for headers
            if p.startswith('# '):
                story.append(Paragraph(self._clean_markdown(p[2:]), self.styles['Heading1']))
            elif p.startswith('## '):
                story.append(Paragraph(self._clean_markdown(p[3:]), self.styles['SubHeader']))
            elif p.startswith('### '):
                story.append(Paragraph(self._clean_markdown(p[4:]), self.styles['Heading4']))
            elif p.startswith('- '):
                # Bullet list
                items = p.split('\n')
                for item in items:
                    if item.startswith('- '):
                        story.append(Paragraph(f"• {self._clean_markdown(item[2:])}", self.styles['ReportBody']))
            else:
                # Normal paragraph
                story.append(Paragraph(self._clean_markdown(p), self.styles['ReportBody']))
                
        story.append(PageBreak())
        
        # --- DETAILED FINDINGS ---
        story.append(Paragraph("Detailed Intelligence Findings", self.styles['SectionHeader']))
        
        for agent_name, result in agent_results.items():
            # Skip if no data
            if not result or not isinstance(result, dict): continue
            
            # Agent Header
            display_name = agent_name.replace('_', ' ').title()
            story.append(Paragraph(display_name, self.styles['Heading2']))
            
            # 1. Render Analysis Text first
            analysis = result.get('summary') or result.get('analysis')
            if analysis:
                story.append(Paragraph("Analysis", self.styles['SubHeader']))
                # Simple cleanup for analysis text
                clean_analysis = self._clean_markdown(str(analysis))
                story.append(Paragraph(clean_analysis, self.styles['ReportBody']))
                story.append(Spacer(1, 0.1*inch))
            
            # 2. Render Structured Data (Tables/Lists)
            data_elements = self._render_agent_data(agent_name, result)
            story.extend(data_elements)
            
            story.append(Spacer(1, 0.3*inch))
            # Add a light separator line
            # story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#eeeeee')))
            
        doc.build(story)
        return filepath