import React from 'react';
import {
  Box,
  Typography,
  Link,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Grid,
  LinearProgress,
  Card,
  CardContent
} from '@mui/material';
import {
  OpenInNew as OpenInNewIcon,
  Article as ArticleIcon,
  Language as LanguageIcon,
  Description as DescriptionIcon,
  Science as ScienceIcon,
  Security as SecurityIcon,
  TrendingUp as TrendingUpIcon,
  Speed as SpeedIcon
} from '@mui/icons-material';
import ReactMarkdown from 'react-markdown';

const AgentResultDisplay = ({ data }) => {
  if (!data) return null;

  // --- Helper Components ---

  const SectionHeader = ({ icon, title, count }) => (
    <Box sx={{
      display: 'flex',
      alignItems: 'center',
      gap: 1.5,
      mb: 3,
      pb: 1.5,
      borderBottom: '1px solid #E2E8F0'
    }}>
      <Box sx={{
        p: 1,
        borderRadius: '10px',
        bgcolor: '#EFF6FF',
        color: '#2563EB',
        display: 'flex',
        boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)'
      }}>
        {icon}
      </Box>
      <Typography variant="h6" sx={{ fontWeight: 700, color: '#1E293B', letterSpacing: '-0.01em' }}>
        {title}
      </Typography>
      {count !== undefined && (
        <Chip
          label={count}
          size="small"
          sx={{
            bgcolor: '#F1F5F9',
            color: '#64748B',
            fontWeight: 600,
            height: 24,
            borderRadius: '6px'
          }}
        />
      )}
    </Box>
  );

  const StatusChip = ({ status }) => {
    let color = '#64748B';
    let bgcolor = '#F1F5F9';

    const s = status?.toLowerCase() || '';
    if (s.includes('recruiting') || s.includes('active')) {
      color = '#16A34A';
      bgcolor = '#DCFCE7';
    } else if (s.includes('completed') || s.includes('granted')) {
      color = '#2563EB';
      bgcolor = '#EFF6FF';
    } else if (s.includes('pending')) {
      color = '#D97706';
      bgcolor = '#FEF3C7';
    }

    return (
      <Chip
        label={status}
        size="small"
        sx={{
          bgcolor,
          color,
          fontWeight: 600,
          fontSize: '0.75rem',
          height: 24,
          borderRadius: '6px'
        }}
      />
    );
  };

  // --- Specialized Renderers ---

  const renderClinicalTrials = (trials, phaseDist, statusDist) => {
    if (!trials || !Array.isArray(trials) || trials.length === 0) return null;
    return (
      <Box sx={{ mb: 5 }}>
        <SectionHeader icon={<ScienceIcon />} title="Clinical Trials Landscape" count={trials.length} />

        {/* Distributions Summary */}
        {(phaseDist || statusDist) && (
          <Box sx={{ mb: 3, display: 'flex', gap: 4, flexWrap: 'wrap' }}>
            {phaseDist && (
              <Box>
                <Typography variant="subtitle2" sx={{ mb: 1, color: '#64748B', fontWeight: 600 }}>Phase Distribution</Typography>
                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                  {Object.entries(phaseDist).map(([phase, count]) => (
                    <Chip
                      key={phase}
                      label={`${phase}: ${count}`}
                      size="small"
                      sx={{ bgcolor: '#F1F5F9', color: '#475569', fontWeight: 500 }}
                    />
                  ))}
                </Box>
              </Box>
            )}
            {statusDist && (
              <Box>
                <Typography variant="subtitle2" sx={{ mb: 1, color: '#64748B', fontWeight: 600 }}>Status Distribution</Typography>
                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                  {Object.entries(statusDist).map(([status, count]) => (
                    <Chip
                      key={status}
                      label={`${status}: ${count}`}
                      size="small"
                      sx={{ bgcolor: '#F1F5F9', color: '#475569', fontWeight: 500 }}
                    />
                  ))}
                </Box>
              </Box>
            )}
          </Box>
        )}

        <Grid container spacing={2}>
          {trials.map((trial, index) => (
            <Grid item xs={12} key={index}>
              <Paper elevation={0} sx={{
                p: 2.5,
                border: '1px solid #E2E8F0',
                borderRadius: 3,
                transition: 'all 0.2s',
                '&:hover': { borderColor: '#CBD5E1', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)' }
              }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600, color: '#1E293B', flex: 1, mr: 2 }}>
                    {trial.title}
                  </Typography>
                  <StatusChip status={trial.status} />
                </Box>

                <Grid container spacing={2} sx={{ mb: 2 }}>
                  <Grid item xs={6} sm={3}>
                    <Typography variant="caption" sx={{ color: '#64748B', display: 'block', mb: 0.5 }}>Phase</Typography>
                    <Chip label={trial.phase || 'N/A'} size="small" variant="outlined" sx={{ borderRadius: '6px', height: 24 }} />
                  </Grid>
                  <Grid item xs={6} sm={3}>
                    <Typography variant="caption" sx={{ color: '#64748B', display: 'block', mb: 0.5 }}>ID</Typography>
                    <Typography variant="body2" sx={{ fontFamily: 'monospace', color: '#475569' }}>{trial.nct_id}</Typography>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="caption" sx={{ color: '#64748B', display: 'block', mb: 0.5 }}>Sponsor</Typography>
                    <Typography variant="body2" sx={{ color: '#475569' }}>{trial.sponsor}</Typography>
                  </Grid>
                </Grid>

                {trial.url && (
                  <Link href={trial.url} target="_blank" rel="noopener noreferrer" sx={{
                    display: 'inline-flex', alignItems: 'center', gap: 0.5, fontSize: '0.875rem', fontWeight: 500, textDecoration: 'none'
                  }}>
                    View Trial Details <OpenInNewIcon sx={{ fontSize: 14 }} />
                  </Link>
                )}
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Box>
    );
  };

  const renderPatents = (patents) => {
    if (!patents || !Array.isArray(patents) || patents.length === 0) return null;
    return (
      <Box sx={{ mb: 5 }}>
        <SectionHeader icon={<SecurityIcon />} title="Intellectual Property" count={patents.length} />
        <TableContainer component={Paper} elevation={0} sx={{ border: '1px solid #E2E8F0', borderRadius: 3 }}>
          <Table>
            <TableHead>
              <TableRow sx={{ bgcolor: '#F8FAFC' }}>
                <TableCell sx={{ fontWeight: 600, color: '#475569' }}>Patent Title</TableCell>
                <TableCell sx={{ fontWeight: 600, color: '#475569' }}>Assignee</TableCell>
                <TableCell sx={{ fontWeight: 600, color: '#475569' }}>Status</TableCell>
                <TableCell sx={{ fontWeight: 600, color: '#475569' }}>Expiry</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {patents.map((patent, index) => (
                <TableRow key={index} hover>
                  <TableCell sx={{ fontWeight: 500, color: '#1E293B' }}>{patent.title}</TableCell>
                  <TableCell sx={{ color: '#64748B' }}>{patent.assignee}</TableCell>
                  <TableCell><StatusChip status={patent.status} /></TableCell>
                  <TableCell sx={{ color: '#64748B', fontFamily: 'monospace' }}>{patent.expiry_date}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
    );
  };

  const renderMarketData = (marketData) => {
    if (!marketData) return null;
    return (
      <Box sx={{ mb: 5 }}>
        <SectionHeader icon={<TrendingUpIcon />} title="Market Intelligence" />
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Paper elevation={0} sx={{ p: 3, bgcolor: '#EFF6FF', borderRadius: 3, height: '100%', border: '1px solid #DBEAFE' }}>
              <Typography variant="subtitle2" sx={{ color: '#2563EB', mb: 1, fontWeight: 600 }}>Market Size</Typography>
              <Typography variant="h4" sx={{ fontWeight: 700, color: '#1E40AF', mb: 1 }}>
                {marketData.market_size_usd && !isNaN(marketData.market_size_usd) 
                  ? `$${(marketData.market_size_usd / 1000000000).toFixed(1)}B`
                  : 'N/A'}
              </Typography>
              <Typography variant="body2" sx={{ color: '#60A5FA' }}>Global Market Valuation</Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper elevation={0} sx={{ p: 3, bgcolor: '#F0FDF4', borderRadius: 3, height: '100%', border: '1px solid #DCFCE7' }}>
              <Typography variant="subtitle2" sx={{ color: '#16A34A', mb: 1, fontWeight: 600 }}>Growth Rate</Typography>
              <Typography variant="h4" sx={{ fontWeight: 700, color: '#15803D', mb: 1 }}>
                {marketData.growth_rate_cagr && !isNaN(marketData.growth_rate_cagr)
                  ? `${marketData.growth_rate_cagr}%`
                  : 'N/A'}
              </Typography>
              <Typography variant="body2" sx={{ color: '#4ADE80' }}>CAGR (Projected)</Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper elevation={0} sx={{ p: 3, border: '1px solid #E2E8F0', borderRadius: 3, height: '100%' }}>
              <Typography variant="subtitle2" sx={{ color: '#64748B', mb: 2, fontWeight: 600 }}>Key Trends</Typography>
              <Box component="ul" sx={{ m: 0, pl: 2, color: '#475569' }}>
                {marketData.key_trends?.map((trend, i) => (
                  <li key={i} style={{ marginBottom: '4px', fontSize: '0.875rem' }}>{trend}</li>
                ))}
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    );
  };

  // --- Main Render ---

  const EXCLUDED_KEYS = [
    'analysis',
    'clinical_trials',
    'trials',
    'patents',
    'market_data',
    'summary',
    'pubmed_papers',
    'web_sources',
    'phase_distribution',
    'status_distribution',
    'total_sources',
    'key_papers',
    'analysis_type'
  ];

  // If data is a string, treat it as markdown
  if (typeof data === 'string') {
    return (
      <Box className="markdown-content" sx={{ p: 1 }}>
        <ReactMarkdown>{data}</ReactMarkdown>
      </Box>
    );
  }

  // If data has an 'analysis' field, use that as primary content
  if (data.analysis) {
    return (
      <Box className="markdown-content" sx={{ p: 1 }}>
        <ReactMarkdown>{data.analysis}</ReactMarkdown>

        {/* Render specialized sections if data exists */}
        {renderClinicalTrials(data.trials || data.clinical_trials, data.phase_distribution, data.status_distribution)}
        {renderPatents(data.patents)}
        {renderMarketData(data.market_data)}

        {/* Fallback for other fields */}
        {Object.entries(data).map(([key, value]) => {
          if (EXCLUDED_KEYS.includes(key)) return null;
          if (typeof value !== 'object' || value === null) return null;

          return (
            <Box key={key} sx={{ mt: 3 }}>
              <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1, textTransform: 'capitalize' }}>
                {key.replace(/_/g, ' ')}
              </Typography>
              <Box component="pre" sx={{
                bgcolor: '#F8FAFC',
                p: 2,
                borderRadius: 2,
                overflow: 'auto',
                fontSize: '0.85rem',
                border: '1px solid #E2E8F0'
              }}>
                {JSON.stringify(value, null, 2)}
              </Box>
            </Box>
          );
        })}
      </Box>
    );
  }

  // Format structured data (Standard View)
  return (
    <Box>
      {/* Summary Section */}
      {data.summary && (
        <Box sx={{ mb: 5 }}>
          <Paper elevation={0} sx={{ p: 4, bgcolor: '#F8FAFC', borderRadius: 3, border: '1px solid #E2E8F0' }}>
            <Box className="markdown-content">
              <ReactMarkdown>{data.summary}</ReactMarkdown>
            </Box>
          </Paper>
        </Box>
      )}

      {/* Render Specialized Sections */}
      {renderClinicalTrials(data.trials || data.clinical_trials, data.phase_distribution, data.status_distribution)}
      {renderPatents(data.patents)}
      {renderMarketData(data.market_data)}

      {/* PubMed Papers Table */}
      {data.pubmed_papers && Array.isArray(data.pubmed_papers) && data.pubmed_papers.length > 0 && (
        <Box sx={{ mb: 5 }}>
          <SectionHeader icon={<ArticleIcon />} title="Scientific Literature" count={data.pubmed_papers.length} />
          <TableContainer component={Paper} elevation={0} sx={{ border: '1px solid #E2E8F0', borderRadius: 3 }}>
            <Table>
              <TableHead>
                <TableRow sx={{ bgcolor: '#F8FAFC' }}>
                  <TableCell sx={{ fontWeight: 600, color: '#475569' }}>Title</TableCell>
                  <TableCell sx={{ fontWeight: 600, color: '#475569' }}>Authors</TableCell>
                  <TableCell sx={{ fontWeight: 600, color: '#475569' }}>Source</TableCell>
                  <TableCell sx={{ fontWeight: 600, color: '#475569' }}>Year</TableCell>
                  <TableCell sx={{ fontWeight: 600, color: '#475569' }}>Action</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {data.pubmed_papers.map((paper, index) => (
                  <TableRow key={index} hover>
                    <TableCell sx={{ fontWeight: 500, color: '#1E293B' }}>{paper.title}</TableCell>
                    <TableCell sx={{ color: '#64748B' }}>
                      {paper.authors && Array.isArray(paper.authors) ? paper.authors.slice(0, 2).join(', ') + '...' : 'N/A'}
                    </TableCell>
                    <TableCell sx={{ color: '#64748B' }}>{paper.source}</TableCell>
                    <TableCell sx={{ color: '#64748B' }}>{paper.pubdate}</TableCell>
                    <TableCell>
                      {paper.url && (
                        <Link href={paper.url} target="_blank" rel="noopener noreferrer" sx={{
                          display: 'inline-flex', alignItems: 'center', gap: 0.5, fontWeight: 500, textDecoration: 'none'
                        }}>
                          View <OpenInNewIcon sx={{ fontSize: 16 }} />
                        </Link>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      )}

      {/* Web Sources Cards */}
      {data.web_sources && Array.isArray(data.web_sources) && data.web_sources.length > 0 && (
        <Box sx={{ mb: 5 }}>
          <SectionHeader icon={<LanguageIcon />} title="Web Intelligence" count={data.web_sources.length} />
          <Grid container spacing={2}>
            {data.web_sources.map((source, index) => (
              <Grid item xs={12} md={6} key={index}>
                <Paper elevation={0} sx={{
                  p: 3,
                  height: '100%',
                  border: '1px solid #E2E8F0',
                  borderRadius: 3,
                  transition: 'all 0.2s',
                  '&:hover': { borderColor: '#2563EB', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)' }
                }}>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1, lineHeight: 1.4 }}>
                    {source.title || 'Untitled Source'}
                  </Typography>
                  {source.snippet && (
                    <Typography variant="body2" sx={{ color: '#64748B', mb: 2, display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                      {source.snippet}
                    </Typography>
                  )}
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 'auto' }}>
                    {source.source && <Chip label={source.source} size="small" sx={{ bgcolor: '#F1F5F9', color: '#475569' }} />}
                    {source.url && (
                      <Link href={source.url} target="_blank" rel="noopener noreferrer" sx={{
                        display: 'inline-flex', alignItems: 'center', gap: 0.5, fontSize: '0.875rem', fontWeight: 500, textDecoration: 'none'
                      }}>
                        Visit <OpenInNewIcon sx={{ fontSize: 14 }} />
                      </Link>
                    )}
                  </Box>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}

      {/* Fallback for other fields in Standard View */}
      {Object.entries(data).map(([key, value]) => {
        if (EXCLUDED_KEYS.includes(key)) return null;
        if (typeof value !== 'object' || value === null) return null;

        return (
          <Box key={key} sx={{ mt: 3 }}>
            <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1, textTransform: 'capitalize' }}>
              {key.replace(/_/g, ' ')}
            </Typography>
            <Box component="pre" sx={{
              bgcolor: '#F8FAFC',
              p: 2,
              borderRadius: 2,
              overflow: 'auto',
              fontSize: '0.85rem',
              border: '1px solid #E2E8F0'
            }}>
              {JSON.stringify(value, null, 2)}
            </Box>
          </Box>
        );
      })}
    </Box>
  );
};

export default AgentResultDisplay;
